from __future__ import annotations

import asyncio
import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import time
from dataclasses import dataclass
from typing import Dict, Optional, Callable, Awaitable, Union


@dataclass
class ProxyConfig:
    """Configuration for the HTTP proxy."""
    url: str
    headers: Optional[Dict[str, str]] = None


@dataclass
class ServerHandlers:
    """Handlers for proxy server lifecycle events."""
    on_listen: Optional[Union[Callable[[], None], Callable[[], Awaitable[None]]]] = None
    on_close: Optional[Union[Callable[[], None], Callable[[], Awaitable[None]]]] = None


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    """HTTP proxy handler that forwards requests to a target server."""
    
    def __init__(self, target_host: str, custom_headers: Dict[str, str], *args, **kwargs):
        self.target_host = target_host
        self.custom_headers = custom_headers
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.proxy_request('GET')

    def do_POST(self):
        self.proxy_request('POST')

    def do_PUT(self):
        self.proxy_request('PUT')

    def do_DELETE(self):
        self.proxy_request('DELETE')

    def do_PATCH(self):
        self.proxy_request('PATCH')

    def do_HEAD(self):
        self.proxy_request('HEAD')

    def do_OPTIONS(self):
        self.proxy_request('OPTIONS')

    def proxy_request(self, method):
        try:
            # Build target URL
            target_url = self.target_host + self.path

            # Get request body for POST/PUT/PATCH
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # Prepare headers
            headers = {}

            # Copy original headers (excluding hop-by-hop headers)
            skip_headers = {
                'host', 'connection', 'upgrade', 'proxy-connection',
                'proxy-authenticate', 'proxy-authorization', 'te', 'trailers'
            }

            for key, value in self.headers.items():
                if key.lower() not in skip_headers:
                    headers[key] = value

            # Add custom headers
            headers.update(self.custom_headers)

            # Create request
            req = urllib.request.Request(
                target_url,
                data=body,
                headers=headers,
                method=method
            )

            # Make the request
            try:
                with urllib.request.urlopen(req, timeout=30) as response:
                    # Check if this is an SSE endpoint
                    content_type = response.headers.get('Content-Type', '')
                    is_sse = 'text/event-stream' in content_type

                    # Send response status
                    self.send_response(response.status)

                    # Send response headers
                    for key, value in response.headers.items():
                        if key.lower() not in ['connection', 'transfer-encoding']:
                            self.send_header(key, value)

                    # Add CORS headers if needed
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, PATCH, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')

                    self.end_headers()

                    if method == 'HEAD':
                        return

                    # Handle SSE streaming
                    if is_sse:
                        self.handle_sse_stream(response)
                    else:
                        # Handle regular response
                        self.wfile.write(response.read())

            except urllib.error.HTTPError as e:
                # Forward HTTP errors
                self.send_response(e.code)

                # Copy error response headers
                for key, value in e.headers.items():
                    if key.lower() not in ['connection', 'transfer-encoding']:
                        self.send_header(key, value)

                self.end_headers()

                if method != 'HEAD':
                    self.wfile.write(e.read())

        except urllib.error.URLError as e:
            # Network error
            self.send_error(502, f"Bad Gateway: {str(e)}")

        except Exception as e:
            # Other errors
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def handle_sse_stream(self, response):
        """Handle Server-Sent Events streaming"""
        try:
            while True:
                chunk = response.read(8192)
                if not chunk:
                    break

                self.wfile.write(chunk)
                self.wfile.flush()

        except Exception as e:
            print(f"SSE streaming error: {e}")

    def log_message(self, format, *args):
        """Custom logging to show proxy activity"""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {self.address_string()} - {format % args}")


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """Multi-threaded HTTP server for handling concurrent requests"""
    allow_reuse_address = True
    daemon_threads = True


async def start_proxy(
        port: int,
        config: ProxyConfig,
        handlers: Optional[ServerHandlers] = None
) -> None:
    """Start an HTTP proxy server.
    
    Args:
        port: Local port to listen on
        config: Proxy configuration
        handlers: Optional server lifecycle handlers
    """
    
    if handlers and handlers.on_listen:
        if asyncio.iscoroutinefunction(handlers.on_listen):
            await handlers.on_listen()
        else:
            handlers.on_listen()

    # Create handler class with configuration
    def handler_factory(*args, **kwargs):
        return ProxyHandler(config.url, config.headers or {}, *args, **kwargs)

    httpd = None
    try:
        httpd = ThreadedHTTPServer(("", port), handler_factory)
        
        # Run the server in a separate thread to avoid blocking the event loop
        loop = asyncio.get_event_loop()
        server_task = loop.run_in_executor(None, httpd.serve_forever)
        
        await server_task
        
    except KeyboardInterrupt:
        print("\nShutting down proxy server...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        # Ensure server is properly shut down
        if httpd:
            httpd.shutdown()
            httpd.server_close()
            
        # Call the on_close handler
        if handlers and handlers.on_close:
            if asyncio.iscoroutinefunction(handlers.on_close):
                await handlers.on_close()
            else:
                handlers.on_close()


def stream_logs(config: ProxyConfig, log_type: str) -> None:
    """Stream logs from the target server.
    
    Args:
        config: Proxy configuration
        log_type: Type of logs to stream ('stdout' or 'stderr')
    """
    import socket
    from urllib.parse import urlparse

    parsed = urlparse(config.url)
    host = parsed.hostname or 'localhost'
    port = parsed.port or (443 if parsed.scheme == 'https' else 80)

    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        request = f"GET /logs/main?type={log_type} HTTP/1.1\r\nHost: {host}\r\n\r\n"
        sock.send(request.encode())

        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode('utf-8', errors='ignore'), end='')

    except Exception as e:
        print(f"[*] Error streaming logs: {e}")
    finally:
        if sock:
            sock.close()
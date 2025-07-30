from __future__ import annotations
import asyncio
import json
from pathlib import Path

import click
from rich.console import Console
from rich.status import Status

from hcli.lib.api.cloud import cloud
from hcli.lib.api.share import share
from hcli.lib.config import config_store
from hcli.lib.auth import get_auth_service
from hcli.lib.proxy.http_proxy import start_proxy, ProxyConfig, ServerHandlers

console = Console()


@click.command()
@click.option("-p", "--port", type=int, default=9999, help="Local port to listen on")
@click.option("-t", "--tool", required=True, help="Tool to expose [api,mcp]")
@click.option("-f", "--force", is_flag=True, help="Force new upload binary (don't use checksum cache)")
@click.argument("binary", type=click.Path(exists=True, path_type=Path))
def analyze(port: int, tool: str, force: bool, binary: Path) -> None:
    """Analyze a binary using IDA cloud."""
    asyncio.run(_analyze_async(port, tool, force, binary))


async def _analyze_async(port: int, tool: str, force: bool, binary: Path) -> None:
    """Async implementation of analyze command."""
    # Check authentication
    auth_service = get_auth_service()
    if not auth_service.is_logged_in():
        console.print("[red]Error: Not logged in. Please run 'hcli login' first.[/red]")
        return

    with Status("Checking for open sessions...", console=console) as status:
        sessions = await cloud.get_sessions()

        if sessions:
            for session in sessions:
                status.update(f"Closing session [{session.sessionId}]")
                await cloud.delete_session(session.sessionId)

    console.print("[green]✓[/green] Sessions checked")

    with Status("Uploading binary...", console=console) as status:
        result = await share.upload_file(str(binary), "private", force)

    console.print(f"[green]✓[/green] Binary uploaded and available at {result.url}")

    input_code = result.code

    with Status("Launching IDA cloud session...", console=console) as status:
        session = await cloud.create_session(tool, {"input_code": input_code})
        config_store.set_object("hcli.cloud.session", session)

    console.print(
        f"[green]✓[/green] IDA cloud session started [{session['sessionId']}]. It will stay open for 10 minutes.")

    # Create proxy configuration
    proxy_config = ProxyConfig(
        url="https://api.hcli.run/",
        headers={
            "x-session-id": session["sessionId"],
            "x-api-key": auth_service.get_api_key(),
        }
    )

    if tool == "mcp":
        server_name = "hcli_ida_mcp_server"
        claude_config_sample = {
            server_name: {
                "command": "npx",
                "args": [
                    "mcp-remote",
                    f"http://127.0.0.1:{port}/sse"
                ]
            }
        }

        console.print("If you are using Claude, you can use the following MCP server configuration:")
        console.print(json.dumps(claude_config_sample, indent=2))

    # Create server handlers
    def on_listen():
        console.print(f"[green]✓[/green] Proxy server started on http://127.0.0.1:{port}")

    async def on_close():
        with Status("Stopping IDA cloud session...", console=console):
            try:
                await cloud.delete_session(session["sessionId"])
            except Exception:
                pass
        console.print(f"[green]✓[/green] Stopping {tool.upper()} proxy server...")

    handlers = ServerHandlers(on_listen=on_listen, on_close=on_close)

    await start_proxy(port, proxy_config, handlers)

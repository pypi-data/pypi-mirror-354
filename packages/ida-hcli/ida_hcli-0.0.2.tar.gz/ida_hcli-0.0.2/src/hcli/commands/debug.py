from __future__ import annotations
import click
from rich.console import Console
from rich.prompt import Prompt

from hcli.lib.auth import get_auth_service
from hcli.lib.commands import async_command
from hcli.lib.config import config_store

console = Console()

@click.group()
def debug():
    """Debug commands for testing authentication flows."""
    pass

@debug.command()
@click.option('--email', help='Mock email to use for testing')
@async_command
async def mock_login(email: str = None) -> None:
    """Mock login for testing without OAuth flow."""
    auth_service = get_auth_service()
    
    if not email:
        email = Prompt.ask("Mock email", default="test@hexrays.com")
    
    console.print(f"[yellow]Setting up mock session for {email}[/yellow]")
    
    # Create a mock session directly in the auth service
    # This bypasses the OAuth flow for testing
    class MockUser:
        def __init__(self, email: str):
            self.email = email
            self.id = "mock-user-id"
    
    class MockSession:
        def __init__(self, email: str):
            self.user = MockUser(email)
            self.access_token = "mock-access-token"
            self.refresh_token = "mock-refresh-token"
    
    # Set mock session
    auth_service.session = MockSession(email)
    auth_service.user = MockUser(email)
    
    console.print(f"[green]Mock login successful for {email}[/green]")
    await auth_service.show_login_info()

@debug.command()
@async_command
async def clear_mock() -> None:
    """Clear mock login session."""
    auth_service = get_auth_service()
    
    # Clear mock session
    auth_service.session = None
    auth_service.user = None
    
    console.print("[green]Mock session cleared[/green]")

@debug.command()
@async_command
async def test_auth() -> None:
    """Test authentication status and token retrieval."""
    auth_service = get_auth_service()
    
    console.print(f"[blue]Is logged in:[/blue] {auth_service.is_logged_in()}")
    console.print(f"[blue]Auth type:[/blue] {auth_service.get_auth_type()}")
    
    user = await auth_service.get_user()
    console.print(f"[blue]User:[/blue] {user}")
    
    api_key = auth_service.get_api_key()
    console.print(f"[blue]API Key:[/blue] {'*' * 8 if api_key else 'None'}")
    
    access_token = auth_service.get_access_token()
    console.print(f"[blue]Access Token:[/blue] {'*' * 8 if access_token else 'None'}")

@debug.command()
@click.option('--error-type', type=click.Choice(['network', 'auth', 'timeout']), help='Type of error to simulate')
@async_command  
async def simulate_error(error_type: str = None) -> None:
    """Simulate various login errors for testing error handling."""
    if not error_type:
        error_type = Prompt.ask("Error type", choices=["network", "auth", "timeout"], default="auth")
    
    console.print(f"[yellow]Simulating {error_type} error...[/yellow]")
    
    if error_type == "network":
        console.print("[red]Error: Network connection failed[/red]")
        console.print("[red]httpx.ConnectError: Could not connect to authentication server[/red]")
    elif error_type == "auth":
        console.print("[red]Error: Authentication failed[/red]")
        console.print("[red]401 Unauthorized: Invalid credentials[/red]")
    elif error_type == "timeout":
        console.print("[red]Error: Authentication timeout[/red]")
        console.print("[red]TimeoutError: OAuth flow timed out after 120 seconds[/red]")

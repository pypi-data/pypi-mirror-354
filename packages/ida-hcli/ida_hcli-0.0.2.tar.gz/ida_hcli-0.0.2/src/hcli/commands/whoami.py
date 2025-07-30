from __future__ import annotations
import click
from rich.console import Console

from hcli.lib.auth import get_auth_service
from hcli.lib.commands import async_command

console = Console()

@click.command()
def whoami() -> None:
    """Display the current logged in user."""
    auth_service = get_auth_service()
    
    # Initialize auth service
    auth_service.init()
    
    # Show login information
    auth_service.show_login_info()

from __future__ import annotations

import click
from rich.console import Console

from hcli.lib.auth import get_auth_service

console = Console()

@click.command()
def logout() -> None:
    """Logout from hex-rays portal."""
    auth_service = get_auth_service()
    
    try:
        auth_service.logout()
        console.print("[green]Successfully logged out.[/green]")
    except Exception as e:
        console.print(f"[red]Error during logout: {e}[/red]")

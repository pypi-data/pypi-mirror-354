from __future__ import annotations
import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.prompt import Prompt

from hcli.lib.auth import get_auth_service
from hcli.lib.api.share import share
from hcli.lib.commands import async_command, auth_command

console = Console()

def get_email_domain(email: str) -> str:
    """Extract domain from email address."""
    return email.split('@')[-1] if '@' in email else ''

@auth_command()
@click.argument('path', type=click.Path(exists=True, path_type=Path))
@click.option('-a', '--acl', 
              type=click.Choice(['public', 'private', 'authenticated', 'domain']),
              help='Access control level (public, private, authenticated, domain)')
@click.option('-c', '--code', 
              help='Upload a new version for an existing code')
@click.option('-f', '--force', is_flag=True, 
              help='Upload a new version for an existing code')
@async_command
async def put(path: Path, acl: Optional[str], code: Optional[str], force: bool) -> None:
    """Upload a shared file."""
    
    # Validate file exists
    if not path.exists():
        console.print(f"[red]Error: File not found: {path}[/red]")
        raise click.Abort()
    
    if not path.is_file():
        console.print(f"[red]Error: Path is not a file: {path}[/red]")
        raise click.Abort()
    
    # Get user info for domain ACL
    auth_service = get_auth_service()
    user = auth_service.get_user()
    domain = get_email_domain(user['email']) if user else ''
    
    # Determine ACL if not provided
    if not acl:
        console.print("\n[bold]Choose access level:[/bold]")
        console.print("1. [cyan]private[/cyan] - Just for me")
        console.print(f"2. [yellow]domain[/yellow] - Anyone from my domain (@{domain})")
        console.print("3. [blue]authenticated[/blue] - Anyone authenticated with the link")
        console.print("4. [green]public[/green] - Anyone with the link")
        
        choice = Prompt.ask("Select access level", choices=["1", "2", "3", "4"], default="3")
        acl_map = {"1": "private", "2": "domain", "3": "authenticated", "4": "public"}
        acl = acl_map[choice]
    
    # Conflicts check
    if force and code:
        console.print("[red]Error: --force and --code cannot be used together[/red]")
        raise click.Abort()
    
    try:
        # Upload the file
        with console.status("[bold green]Preparing upload..."):
            result = await share.upload_file(str(path), acl, force, code)
        
        console.print(f"[green]✓ File uploaded successfully![/green]")
        console.print(f"[bold]Share Code:[/bold] {result.code}")
        console.print(f"[bold]Share URL:[/bold] {result.url}")
        console.print(f"[bold]Download URL:[/bold] {result.download_url}")
        
    except Exception as e:
        console.print(f"[red]Error uploading file: {e}[/red]")
        raise click.Abort()

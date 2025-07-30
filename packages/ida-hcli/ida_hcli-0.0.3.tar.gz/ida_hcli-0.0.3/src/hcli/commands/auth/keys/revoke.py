from __future__ import annotations
import sys
from typing import List
import click
from rich.console import Console
from rich.prompt import Confirm
from rich.table import Table

from hcli.lib.commands import async_command, require_auth
from hcli.lib.api.keys import keys, ApiKey

console = Console()

def display_keys_for_selection(api_keys: List[ApiKey]) -> None:
    """Display keys in a table with numbers for selection."""
    table = Table(title="Select API Key to Revoke")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Name", style="green")
    table.add_column("Created", style="yellow")
    table.add_column("Requests", style="magenta", justify="right")
    
    for i, key in enumerate(api_keys, 1):
        table.add_row(
            str(i),
            f"[underline]{key.name}[/underline]",
            key.created_at[:10] if key.created_at else "Unknown",  # Show just date part
            str(key.request_count)
        )
    
    console.print(table)

@click.command()
@require_auth  
@async_command
async def revoke() -> None:
    """Revoke an API key."""
    try:
        # Get all keys
        api_keys = await keys.get_keys()
        
        if not api_keys:
            console.print("[yellow]No API keys found to revoke.[/yellow]")
            return
        
        # Display keys for selection
        display_keys_for_selection(api_keys)
        
        # Get user selection
        while True:
            try:
                selection = console.input("\nEnter the number of the key to revoke (or 'q' to quit): ")
                if selection.lower() in ['q', 'quit', 'exit']:
                    console.print("[yellow]Operation cancelled.[/yellow]")
                    return
                
                index = int(selection) - 1
                if 0 <= index < len(api_keys):
                    selected_key = api_keys[index]
                    break
                else:
                    console.print(f"[red]Please enter a number between 1 and {len(api_keys)}[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number or 'q' to quit[/red]")
        
        # Confirm revocation
        if not Confirm.ask(f"Do you want to revoke the key named '[bold]{selected_key.name}[/bold]'?"):
            console.print("[yellow]Revocation cancelled.[/yellow]")
            return
        
        # Revoke the key
        console.print(f"[blue]Revoking API key '[bold]{selected_key.name}[/bold]'...[/blue]")
        await keys.revoke_key(selected_key.name)
        console.print(f"[green]API key '[bold]{selected_key.name}[/bold]' has been revoked.[/green]")
    
    except Exception as e:
        console.print(f"[red]Failed to revoke API key: {e}[/red]")
        sys.exit(1)
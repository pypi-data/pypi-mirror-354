from __future__ import annotations
import asyncio

import click
from rich.console import Console
from rich.table import Table

from hcli.lib.api.plugins import plugins

console = Console()

async def _list_plugin_groups() -> None:
    """List all plugin groups/categories."""
    try:
        # Get plugin categories from API
        categories = await plugins.get_categories()
        
        if not categories:
            console.print("[yellow]No plugin categories found.[/yellow]")
            return
        
        # Create Rich table for display
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Category", style="cyan")
        table.add_column("Plugins", style="green", justify="right")
        table.add_column("ID", style="dim")
        
        # Sort categories by name
        sorted_categories = sorted(categories, key=lambda c: c.name.lower())
        
        # Add categories to table
        for category in sorted_categories:
            table.add_row(
                category.name,
                str(category.pluginCount),
                category.id
            )
        
        console.print(f"\n[bold]Plugin Categories ({len(categories)} total):[/bold]")
        console.print(table)
        
        total_plugins = sum(cat.pluginCount for cat in categories)
        console.print(f"\n[dim]Total plugins across all categories: {total_plugins}[/dim]")
        console.print("\n[dim]Use 'hcli plugin browse' to explore plugins by category[/dim]")
        console.print("[dim]Use 'hcli plugin search' to search for specific plugins[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error listing plugin groups: {e}[/red]")

@click.command()
def list_groups() -> None:
    """List plugin groups/categories."""
    asyncio.run(_list_plugin_groups())
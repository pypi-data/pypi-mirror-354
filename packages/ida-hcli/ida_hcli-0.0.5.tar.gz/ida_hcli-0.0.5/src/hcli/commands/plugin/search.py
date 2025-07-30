from __future__ import annotations
import asyncio
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from hcli.lib.api.plugins import plugins, PluginQuery
from hcli.lib.util.string import abbreviate

console = Console()

async def _search_plugins(query: Optional[str] = None) -> None:
    """Search for plugins in the repository."""
    try:
        # Search plugins using the API
        search_query = PluginQuery(q=query or "")
        result = await plugins.search(search_query)
        
        if not result.hits:
            console.print("[yellow]No plugins found.[/yellow]")
            return
        
        # Create Rich table for display
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Plugin", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        # Add plugins to table
        for plugin in result.hits:
            plugin_name = Text(plugin.slug, style="bold cyan")
            description = abbreviate(plugin.metadata.repository_description or "", 80)
            table.add_row(plugin_name, description)
        
        console.print(f"\nFound {len(result.hits)} plugin(s):")
        console.print(table)
        
        if result.estimatedTotalHits > len(result.hits):
            console.print(f"\n[dim]Showing {len(result.hits)} of {result.estimatedTotalHits} total results[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error searching plugins: {e}[/red]")

@click.command()
@click.argument('query', required=False)
def search(query: Optional[str] = None) -> None:
    """Search for plugins in the repository."""
    asyncio.run(_search_plugins(query))

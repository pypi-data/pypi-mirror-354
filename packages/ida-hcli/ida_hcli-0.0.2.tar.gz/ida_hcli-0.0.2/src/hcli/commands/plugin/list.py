from __future__ import annotations
import asyncio

import click
from rich.console import Console
from rich.table import Table
from rich.text import Text

from hcli.lib.ida.plugin import get_installed_plugins
from hcli.lib.util.string import abbreviate

console = Console()

async def _list_installed_plugins() -> None:
    """List all installed plugins with their status."""
    try:
        # Get installed plugins (including disabled ones)
        installed = await get_installed_plugins(include_disabled=True)
        
        if not installed:
            console.print("[yellow]No plugins installed.[/yellow]")
            console.print("\nTo install plugins, use: [bold]hcli plugin install <plugin-name>[/bold]")
            console.print("To browse available plugins, use: [bold]hcli plugin browse[/bold]")
            return
        
        # Create Rich table for display
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status", width=8, justify="center")
        table.add_column("Plugin", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        
        # Add plugins to table
        for plugin in installed:
            # Status indicator
            if plugin.disabled:
                status = Text("✘", style="red")
            else:
                status = Text("✓", style="green")
            
            # Plugin name (make it bold and underlined)
            plugin_name = Text(plugin.slug, style="bold cyan")
            
            # Description (truncated)
            description = abbreviate(plugin.metadata.repository_description or "", 80)
            
            table.add_row(status, plugin_name, description)
        
        console.print(f"\n[bold]Installed Plugins ({len(installed)} total):[/bold]")
        console.print(table)
        
        # Show status summary
        enabled_count = len([p for p in installed if not p.disabled])
        disabled_count = len([p for p in installed if p.disabled])
        
        console.print(f"\n[green]✓ {enabled_count} enabled[/green]")
        if disabled_count > 0:
            console.print(f"[red]✘ {disabled_count} disabled[/red]")
        
        console.print("\n[dim]Use 'hcli plugin enable' to enable/disable plugins[/dim]")
        console.print("[dim]Use 'hcli plugin update' to update installed plugins[/dim]")
        console.print("[dim]Use 'hcli plugin uninstall' to remove plugins[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error listing installed plugins: {e}[/red]")

@click.command()
def list_plugins() -> None:
    """List installed plugins."""
    asyncio.run(_list_installed_plugins())

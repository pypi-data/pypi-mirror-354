from __future__ import annotations
import asyncio
import sys
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from hcli.lib.ida.plugin import get_installed_plugins, get_plugin_install_dir
from hcli.lib.util.io import remove_dir

console = Console()

async def _uninstall_plugins(plugin_name: Optional[str] = None) -> None:
    """Uninstall installed plugins with confirmation."""
    try:
        # Get all installed plugins
        installed = await get_installed_plugins(include_disabled=True)
        
        if not installed:
            console.print("[yellow]No plugins installed.[/yellow]")
            return
        
        if plugin_name:
            # Uninstall specific plugin
            plugin_to_remove = None
            for plugin in installed:
                if plugin.slug == plugin_name or plugin.name == plugin_name:
                    plugin_to_remove = plugin
                    break
            
            if not plugin_to_remove:
                console.print(f"[red]Plugin '{plugin_name}' not found in installed plugins.[/red]")
                console.print("Use [bold]hcli plugin list[/bold] to see installed plugins.")
                return
            
            await _uninstall_single_plugin(plugin_to_remove)
        else:
            # Interactive mode - let user select plugins to uninstall
            while True:
                # Display installed plugins
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Index", style="dim", width=6)
                table.add_column("Plugin", style="cyan")
                table.add_column("Status", width=8, justify="center")
                table.add_column("Description", style="white")
                
                for i, plugin in enumerate(installed):
                    status = "[green]✓[/green]" if not plugin.disabled else "[red]✘[/red]"
                    description = plugin.metadata.repository_description or ""
                    if len(description) > 60:
                        description = description[:57] + "..."
                    
                    table.add_row(
                        str(i + 1),
                        plugin.slug,
                        status,
                        description
                    )
                
                console.print("\n[bold]Installed Plugins:[/bold]")
                console.print(table)
                
                console.print("\n[dim]Commands:[/dim]")
                console.print("[dim]  <number> - Uninstall specific plugin[/dim]")
                console.print("[dim]  q        - Quit[/dim]")
                
                # Get user selection
                choice = Prompt.ask(
                    "\nSelect plugin to uninstall",
                    default="q"
                ).strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    break
                else:
                    # Try to parse as plugin number
                    try:
                        plugin_num = int(choice)
                        if 1 <= plugin_num <= len(installed):
                            plugin = installed[plugin_num - 1]
                            
                            success = await _uninstall_single_plugin(plugin)
                            if success:
                                # Remove from installed list for next iteration
                                installed.remove(plugin)
                                
                                if not installed:
                                    console.print("[yellow]No more plugins installed.[/yellow]")
                                    break
                        else:
                            console.print("[red]Invalid plugin number.[/red]")
                    except ValueError:
                        console.print("[red]Invalid command. Enter a number or 'q'.[/red]")
        
    except Exception as e:
        console.print(f"[red]Error uninstalling plugins: {e}[/red]")
        sys.exit(1)

async def _uninstall_single_plugin(plugin) -> bool:
    """Uninstall a single plugin with confirmation."""
    target_path = get_plugin_install_dir(plugin.slug)
    
    console.print(f"\n[bold]Plugin:[/bold] {plugin.slug}")
    if plugin.metadata.repository_description:
        console.print(f"[bold]Description:[/bold] {plugin.metadata.repository_description}")
    console.print(f"[bold]Install path:[/bold] {target_path}")
    
    if Confirm.ask(f"\n[red]Are you sure you want to uninstall '{plugin.slug}'?[/red]"):
        console.print(f"[cyan]Removing plugin {plugin.slug}...[/cyan]")
        
        success = await remove_dir(target_path)
        
        if success:
            console.print(f"[green]✓ Plugin {plugin.slug} uninstalled successfully![/green]")
            console.print(f"[dim]Removed: {target_path}[/dim]")
            console.print("[yellow]Restart IDA to apply changes.[/yellow]")
            return True
        else:
            console.print(f"[red]✗ Failed to uninstall plugin {plugin.slug}[/red]")
            console.print(f"[red]Could not remove directory: {target_path}[/red]")
            return False
    else:
        console.print("[yellow]Uninstallation cancelled.[/yellow]")
        return False

@click.command()
@click.argument('plugin', required=False)
def uninstall(plugin: Optional[str] = None) -> None:
    """Uninstall a plugin."""
    asyncio.run(_uninstall_plugins(plugin))

from __future__ import annotations
import asyncio
import sys
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from hcli.lib.api.plugins import plugins, PluginQuery, Plugin
from hcli.lib.ida.plugin import (
    is_git_installed, is_git_url, get_plugin_from_git_url, 
    get_plugin_install_dir, install_plugin
)
from hcli.lib.util.io import dir_exists, remove_dir

console = Console()

async def _install_plugin(plugin_name: Optional[str] = None) -> None:
    """Install a plugin from repository or Git URL."""
    try:
        # Check if git is installed
        if not await is_git_installed():
            console.print("[red]Git is required for this command. Please install git and try again.[/red]")
            sys.exit(1)
        
        if not plugin_name:
            # If no plugin specified, browse available plugins
            from hcli.commands.plugin.browse import _browse_plugins
            await _browse_plugins()
            return
        
        selected_plugin: Optional[Plugin] = None
        
        # Check if the plugin argument is a git URL
        if is_git_url(plugin_name):
            selected_plugin = get_plugin_from_git_url(plugin_name)
            console.print(f"[cyan]Installing from Git URL: {plugin_name}[/cyan]")
        else:
            # Search for the plugin in the repository
            console.print(f"[cyan]Searching for plugin: {plugin_name}[/cyan]")
            search_result = await plugins.search(PluginQuery(q=plugin_name))
            
            # Check for exact slug match first
            exact_match = None
            for plugin in search_result.hits:
                if plugin.slug == plugin_name:
                    exact_match = plugin
                    break
            
            if exact_match:
                selected_plugin = exact_match
            elif search_result.hits:
                # Show search results and let user choose
                console.print(f"\nFound {len(search_result.hits)} matching plugin(s):")
                
                table = Table(show_header=True, header_style="bold magenta")
                table.add_column("Index", style="dim", width=6)
                table.add_column("Plugin", style="cyan")
                table.add_column("Description", style="white")
                
                for i, plugin in enumerate(search_result.hits):
                    description = plugin.metadata.repository_description or ""
                    if len(description) > 60:
                        description = description[:57] + "..."
                    table.add_row(str(i + 1), plugin.slug, description)
                
                console.print(table)
                
                # Get user selection
                while True:
                    try:
                        choice = Prompt.ask(
                            "\nSelect plugin to install (number)",
                            choices=[str(i + 1) for i in range(len(search_result.hits))],
                            show_choices=False
                        )
                        plugin_index = int(choice) - 1
                        selected_plugin = search_result.hits[plugin_index]
                        break
                    except (ValueError, IndexError):
                        console.print("[red]Invalid selection. Please try again.[/red]")
            else:
                console.print(f"[yellow]No plugins found matching '{plugin_name}'[/yellow]")
                return
        
        if not selected_plugin:
            console.print("[red]Could not determine plugin to install.[/red]")
            return
        
        # Get target installation path
        target_path = get_plugin_install_dir(selected_plugin.slug)
        
        # Check if target directory already exists
        if dir_exists(target_path):
            console.print(f"[yellow]Directory {target_path} already exists.[/yellow]")
            
            if Confirm.ask(f"Do you want to remove {target_path} and reinstall?"):
                if not await remove_dir(target_path):
                    console.print(f"[red]Directory {target_path} could not be removed.[/red]")
                    sys.exit(1)
                console.print(f"[green]Removed existing directory: {target_path}[/green]")
            else:
                console.print("[yellow]Installation cancelled.[/yellow]")
                return
        
        # Confirm installation
        console.print(f"\n[bold]Plugin:[/bold] {selected_plugin.slug}")
        if selected_plugin.metadata.repository_description:
            console.print(f"[bold]Description:[/bold] {selected_plugin.metadata.repository_description}")
        console.print(f"[bold]Install path:[/bold] {target_path}")
        
        if Confirm.ask(f"\nDo you want to install plugin '{selected_plugin.slug}'?"):
            console.print(f"[cyan]Installing plugin {selected_plugin.slug}...[/cyan]")
            
            success = await install_plugin(selected_plugin, target_path)
            
            if success:
                console.print(f"[green]✓ Plugin {selected_plugin.slug} installed successfully![/green]")
                console.print(f"[dim]Location: {target_path}[/dim]")
                console.print("[yellow]Restart IDA to see the plugin in action.[/yellow]")
            else:
                console.print(f"[red]✗ Failed to install plugin {selected_plugin.slug}[/red]")
                sys.exit(1)
        else:
            console.print("[yellow]Installation cancelled.[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error installing plugin: {e}[/red]")
        sys.exit(1)

@click.command()
@click.argument('plugin', required=False)
def install(plugin: Optional[str] = None) -> None:
    """Install a plugin from repository or Git URL."""
    asyncio.run(_install_plugin(plugin))

from __future__ import annotations
import asyncio
from typing import List, Dict, Any

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from hcli.lib.api.plugins import plugins, Plugin, PluginCategoryInfo
from hcli.lib.util.string import abbreviate

console = Console()

async def _browse_plugins() -> None:
    """Browse plugins by category with interactive selection."""
    try:
        # Fetch categories and plugins
        console.print("[cyan]Loading plugin categories...[/cyan]")
        categories = await plugins.get_categories()
        all_plugins = await plugins.get_plugins()
        
        if not categories:
            console.print("[yellow]No categories found.[/yellow]")
            return
        
        # Group plugins by category
        plugins_by_category: Dict[str, List[Plugin]] = {}
        for plugin in all_plugins.hits:
            if plugin.categories:
                for category in plugin.categories:
                    if category.id not in plugins_by_category:
                        plugins_by_category[category.id] = []
                    plugins_by_category[category.id].append(plugin)
        
        while True:
            # Display categories table
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Index", style="dim", width=6)
            table.add_column("Category", style="cyan")
            table.add_column("Plugins", style="green", justify="right")
            
            for i, category in enumerate(categories):
                plugin_count = len(plugins_by_category.get(category.id, []))
                table.add_row(str(i + 1), category.name, str(plugin_count))
            
            console.print("\n[bold]Plugin Categories:[/bold]")
            console.print(table)
            
            # Get user selection
            try:
                choice = Prompt.ask(
                    "\nSelect category (number) or 'q' to quit",
                    choices=[str(i + 1) for i in range(len(categories))] + ['q'],
                    default='q'
                )
                
                if choice.lower() == 'q':
                    break
                
                category_index = int(choice) - 1
                selected_category = categories[category_index]
                category_plugins = plugins_by_category.get(selected_category.id, [])
                
                if not category_plugins:
                    console.print(f"[yellow]No plugins found in category '{selected_category.name}'[/yellow]")
                    continue
                
                # Display plugins in selected category
                await _display_category_plugins(selected_category, category_plugins)
                
            except (ValueError, IndexError):
                console.print("[red]Invalid selection. Please try again.[/red]")
                
    except Exception as e:
        console.print(f"[red]Error browsing plugins: {e}[/red]")

async def _display_category_plugins(category: PluginCategoryInfo, category_plugins: List[Plugin]) -> None:
    """Display plugins in a specific category."""
    while True:
        # Display plugins table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Index", style="dim", width=6)
        table.add_column("Plugin", style="cyan")
        table.add_column("Description", style="white")
        
        for i, plugin in enumerate(category_plugins):
            description = abbreviate(plugin.metadata.repository_description or "", 60)
            table.add_row(str(i + 1), plugin.slug, description)
        
        console.print(f"\n[bold]Plugins in '{category.name}' ({len(category_plugins)} total):[/bold]")
        console.print(table)
        
        # Get user selection
        try:
            choice = Prompt.ask(
                "\nSelect plugin (number), 'i <number>' to install, or 'b' to go back",
                default='b'
            )
            
            if choice.lower() == 'b':
                break
            
            # Handle install command
            if choice.lower().startswith('i '):
                try:
                    plugin_index = int(choice[2:]) - 1
                    if 0 <= plugin_index < len(category_plugins):
                        selected_plugin = category_plugins[plugin_index]
                        # Import install command and call it
                        from hcli.commands.plugin.install import _install_plugin
                        await _install_plugin(selected_plugin.slug)
                    else:
                        console.print("[red]Invalid plugin number.[/red]")
                except ValueError:
                    console.print("[red]Invalid format. Use 'i <number>' to install.[/red]")
                continue
            
            # Handle plugin selection (just display info)
            try:
                plugin_index = int(choice) - 1
                if 0 <= plugin_index < len(category_plugins):
                    selected_plugin = category_plugins[plugin_index]
                    _display_plugin_info(selected_plugin)
                else:
                    console.print("[red]Invalid plugin number.[/red]")
            except ValueError:
                console.print("[red]Invalid selection. Please try again.[/red]")
                
        except (ValueError, IndexError):
            console.print("[red]Invalid selection. Please try again.[/red]")

def _display_plugin_info(plugin: Plugin) -> None:
    """Display detailed information about a plugin."""
    console.print(f"\n[bold cyan]{plugin.slug}[/bold cyan]")
    console.print(f"[white]{plugin.metadata.repository_description}[/white]")
    
    if plugin.metadata.repository_owner:
        console.print(f"Owner: [yellow]{plugin.metadata.repository_owner}[/yellow]")
    
    if plugin.url:
        console.print(f"URL: [blue]{plugin.url}[/blue]")
    
    if plugin.categories:
        categories_str = ", ".join([cat.name for cat in plugin.categories])
        console.print(f"Categories: [green]{categories_str}[/green]")
    
    if plugin.updated_at:
        console.print(f"Last updated: [dim]{plugin.updated_at}[/dim]")
    
    console.print(f"\nTo install: [bold]hcli plugin install {plugin.slug}[/bold]")

@click.command()
def browse() -> None:
    """Browse plugins by category."""
    asyncio.run(_browse_plugins())

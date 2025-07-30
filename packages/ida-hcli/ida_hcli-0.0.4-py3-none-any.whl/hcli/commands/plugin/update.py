from __future__ import annotations
import asyncio
import sys
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from hcli.lib.ida.plugin import get_installed_plugins, update_plugin

console = Console()

async def _update_plugins(plugin_name: Optional[str] = None) -> None:
    """Update installed plugins."""
    try:
        # Get all installed plugins
        installed = await get_installed_plugins(include_disabled=True)
        
        if not installed:
            console.print("[yellow]No plugins installed.[/yellow]")
            console.print("Install plugins first using: [bold]hcli plugin install[/bold]")
            return
        
        if plugin_name:
            # Update specific plugin
            plugin_to_update = None
            for plugin in installed:
                if plugin.slug == plugin_name or plugin.name == plugin_name:
                    plugin_to_update = plugin
                    break
            
            if not plugin_to_update:
                console.print(f"[red]Plugin '{plugin_name}' not found in installed plugins.[/red]")
                console.print("Use [bold]hcli plugin list[/bold] to see installed plugins.")
                return
            
            console.print(f"[cyan]Updating plugin: {plugin_to_update.slug}[/cyan]")
            
            if Confirm.ask(f"Do you want to update '{plugin_to_update.slug}'?"):
                success = await update_plugin(plugin_to_update.slug)
                
                if success:
                    console.print(f"[green]✓ Plugin {plugin_to_update.slug} updated successfully![/green]")
                    console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                else:
                    console.print(f"[red]✗ Failed to update plugin {plugin_to_update.slug}[/red]")
                    sys.exit(1)
            else:
                console.print("[yellow]Update cancelled.[/yellow]")
        else:
            # Interactive mode - let user select plugins to update
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
                console.print("[dim]  <number> - Update specific plugin[/dim]")
                console.print("[dim]  all      - Update all plugins[/dim]")
                console.print("[dim]  q        - Quit[/dim]")
                
                # Get user selection
                choice = Prompt.ask(
                    "\nSelect plugin to update or command",
                    default="q"
                ).strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    break
                elif choice == 'all':
                    # Update all plugins
                    if Confirm.ask(f"Do you want to update all {len(installed)} plugins?"):
                        updated_count = 0
                        failed_count = 0
                        
                        for plugin in installed:
                            console.print(f"[cyan]Updating {plugin.slug}...[/cyan]")
                            success = await update_plugin(plugin.slug)
                            
                            if success:
                                console.print(f"[green]✓ {plugin.slug} updated[/green]")
                                updated_count += 1
                            else:
                                console.print(f"[red]✗ Failed to update {plugin.slug}[/red]")
                                failed_count += 1
                        
                        console.print(f"\n[bold]Update Summary:[/bold]")
                        console.print(f"[green]✓ {updated_count} plugins updated[/green]")
                        if failed_count > 0:
                            console.print(f"[red]✗ {failed_count} plugins failed[/red]")
                        
                        if updated_count > 0:
                            console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                    else:
                        console.print("[yellow]Update cancelled.[/yellow]")
                else:
                    # Try to parse as plugin number
                    try:
                        plugin_num = int(choice)
                        if 1 <= plugin_num <= len(installed):
                            plugin = installed[plugin_num - 1]
                            
                            console.print(f"[cyan]Updating plugin: {plugin.slug}[/cyan]")
                            
                            if Confirm.ask(f"Do you want to update '{plugin.slug}'?"):
                                success = await update_plugin(plugin.slug)
                                
                                if success:
                                    console.print(f"[green]✓ Plugin {plugin.slug} updated successfully![/green]")
                                    console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                                else:
                                    console.print(f"[red]✗ Failed to update plugin {plugin.slug}[/red]")
                            else:
                                console.print("[yellow]Update cancelled.[/yellow]")
                        else:
                            console.print("[red]Invalid plugin number.[/red]")
                    except ValueError:
                        console.print("[red]Invalid command. Enter a number, 'all', or 'q'.[/red]")
        
    except Exception as e:
        console.print(f"[red]Error updating plugins: {e}[/red]")
        sys.exit(1)

@click.command()
@click.argument('plugin', required=False)
def update_plugin_cmd(plugin: Optional[str] = None) -> None:
    """Update installed plugins."""
    asyncio.run(_update_plugins(plugin))

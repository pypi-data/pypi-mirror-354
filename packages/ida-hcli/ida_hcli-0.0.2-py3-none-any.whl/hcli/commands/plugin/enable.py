from __future__ import annotations
import asyncio
from typing import List

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from hcli.lib.ida.plugin import get_installed_plugins, toggle_plugin

console = Console()

async def _enable_disable_plugins() -> None:
    """Enable or disable installed plugins with multi-select interface."""
    try:
        # Get all installed plugins (including disabled)
        plugins = await get_installed_plugins(include_disabled=True)
        
        if not plugins:
            console.print("[yellow]No plugins installed.[/yellow]")
            console.print("Install plugins first using: [bold]hcli plugin install[/bold]")
            return
        
        while True:
            # Display current plugin status
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Index", style="dim", width=6)
            table.add_column("Status", width=8, justify="center")
            table.add_column("Plugin", style="cyan")
            table.add_column("Description", style="white")
            
            for i, plugin in enumerate(plugins):
                status = "[green]✓[/green]" if not plugin.disabled else "[red]✘[/red]"
                description = plugin.metadata.repository_description or ""
                if len(description) > 60:
                    description = description[:57] + "..."
                
                table.add_row(
                    str(i + 1),
                    status,
                    plugin.slug,
                    description
                )
            
            console.print("\n[bold]Installed Plugins:[/bold]")
            console.print(table)
            
            console.print("\n[dim]Commands:[/dim]")
            console.print("[dim]  <number>     - Toggle plugin enable/disable status[/dim]")
            console.print("[dim]  enable <num> - Enable specific plugin[/dim]")
            console.print("[dim]  disable <num> - Disable specific plugin[/dim]")
            console.print("[dim]  all          - Enable all plugins[/dim]")
            console.print("[dim]  none         - Disable all plugins[/dim]")
            console.print("[dim]  q            - Quit[/dim]")
            
            # Get user command
            command = Prompt.ask(
                "\nEnter command",
                default="q"
            ).strip().lower()
            
            if command == 'q' or command == 'quit':
                break
            elif command == 'all':
                # Enable all plugins
                changes_made = False
                for plugin in plugins:
                    if plugin.disabled:
                        success = await toggle_plugin(plugin.slug, True)
                        if success:
                            plugin.disabled = False
                            changes_made = True
                            console.print(f"[green]✓ Enabled {plugin.slug}[/green]")
                        else:
                            console.print(f"[red]✗ Failed to enable {plugin.slug}[/red]")
                
                if changes_made:
                    console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                else:
                    console.print("[dim]All plugins are already enabled.[/dim]")
                    
            elif command == 'none':
                # Disable all plugins
                changes_made = False
                for plugin in plugins:
                    if not plugin.disabled:
                        success = await toggle_plugin(plugin.slug, False)
                        if success:
                            plugin.disabled = True
                            changes_made = True
                            console.print(f"[yellow]✓ Disabled {plugin.slug}[/yellow]")
                        else:
                            console.print(f"[red]✗ Failed to disable {plugin.slug}[/red]")
                
                if changes_made:
                    console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                else:
                    console.print("[dim]All plugins are already disabled.[/dim]")
                    
            elif command.startswith('enable '):
                # Enable specific plugin
                try:
                    plugin_num = int(command.split()[1])
                    if 1 <= plugin_num <= len(plugins):
                        plugin = plugins[plugin_num - 1]
                        if plugin.disabled:
                            success = await toggle_plugin(plugin.slug, True)
                            if success:
                                plugin.disabled = False
                                console.print(f"[green]✓ Enabled {plugin.slug}[/green]")
                                console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                            else:
                                console.print(f"[red]✗ Failed to enable {plugin.slug}[/red]")
                        else:
                            console.print(f"[dim]{plugin.slug} is already enabled.[/dim]")
                    else:
                        console.print("[red]Invalid plugin number.[/red]")
                except (ValueError, IndexError):
                    console.print("[red]Invalid command format. Use: enable <number>[/red]")
                    
            elif command.startswith('disable '):
                # Disable specific plugin
                try:
                    plugin_num = int(command.split()[1])
                    if 1 <= plugin_num <= len(plugins):
                        plugin = plugins[plugin_num - 1]
                        if not plugin.disabled:
                            success = await toggle_plugin(plugin.slug, False)
                            if success:
                                plugin.disabled = True
                                console.print(f"[yellow]✓ Disabled {plugin.slug}[/yellow]")
                                console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                            else:
                                console.print(f"[red]✗ Failed to disable {plugin.slug}[/red]")
                        else:
                            console.print(f"[dim]{plugin.slug} is already disabled.[/dim]")
                    else:
                        console.print("[red]Invalid plugin number.[/red]")
                except (ValueError, IndexError):
                    console.print("[red]Invalid command format. Use: disable <number>[/red]")
                    
            else:
                # Try to parse as a plugin number to toggle
                try:
                    plugin_num = int(command)
                    if 1 <= plugin_num <= len(plugins):
                        plugin = plugins[plugin_num - 1]
                        new_state = not plugin.disabled  # Toggle current state
                        success = await toggle_plugin(plugin.slug, new_state)
                        
                        if success:
                            plugin.disabled = not new_state
                            action = "Enabled" if new_state else "Disabled"
                            color = "green" if new_state else "yellow"
                            console.print(f"[{color}]✓ {action} {plugin.slug}[/{color}]")
                            console.print("[yellow]Restart IDA to apply changes.[/yellow]")
                        else:
                            action = "enable" if new_state else "disable"
                            console.print(f"[red]✗ Failed to {action} {plugin.slug}[/red]")
                    else:
                        console.print("[red]Invalid plugin number.[/red]")
                except ValueError:
                    console.print("[red]Invalid command. Type a number, 'all', 'none', or 'q'.[/red]")
        
    except Exception as e:
        console.print(f"[red]Error managing plugins: {e}[/red]")

@click.command()
def enable() -> None:
    """Enable or disable installed plugins."""
    asyncio.run(_enable_disable_plugins())

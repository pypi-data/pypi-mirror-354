from __future__ import annotations
import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from hcli.lib.commands import async_command
from hcli.lib.registry import Registry, RegistryEntry, type_to_string, value_to_string

console = Console()


def _display_entries(entries: list[RegistryEntry]) -> None:
    """Display registry entries in a table."""
    if not entries:
        console.print("[yellow]No registry entries found.[/yellow]")
        return
    
    table = Table(title="Registry Entries")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Key/Name", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Value", style="yellow")
    
    for i, entry in enumerate(entries):
        table.add_row(
            str(i + 1),
            f"{entry.key}/{entry.name}",
            type_to_string(entry.type),
            str(entry.value)[:50] + ("..." if len(str(entry.value)) > 50 else "")
        )
    
    console.print(table)


@click.command()
@async_command
async def edit_config() -> None:
    """Edit an IDA registry value."""
    registry = Registry.get_registry()
    values = await registry.get_values()
    
    if not values:
        console.print("[yellow]No registry entries found to edit.[/yellow]")
        return
    
    # Display entries
    _display_entries(values)
    
    # Let user select an entry to edit
    while True:
        try:
            choice = Prompt.ask(
                "Enter the index of the entry to edit",
                default="1"
            )
            index = int(choice) - 1
            
            if 0 <= index < len(values):
                selected_entry = values[index]
                break
            else:
                console.print(f"[red]Invalid index. Please enter a number between 1 and {len(values)}.[/red]")
        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
    
    # Show selected entry
    console.print(f"\n[bold]Selected entry:[/bold]")
    console.print(f"Key: {selected_entry.key}")
    console.print(f"Name: {selected_entry.name}")
    console.print(f"Type: {type_to_string(selected_entry.type)}")
    console.print(f"Current value: {selected_entry.value}")
    
    # Get new value
    new_value_str = Prompt.ask(
        "New value",
        default=value_to_string(selected_entry)
    )
    
    # Convert value based on type
    try:
        if selected_entry.type.name == "REG_DWORD":
            new_value = int(new_value_str)
        elif selected_entry.type.name == "REG_BINARY":
            # Convert hex string to bytes
            new_value = bytes.fromhex(new_value_str)
        else:  # REG_SZ
            new_value = new_value_str
    except ValueError as e:
        console.print(f"[red]Invalid value format for {type_to_string(selected_entry.type)}: {e}[/red]")
        return
    
    # Create updated entry
    updated_entry = RegistryEntry(
        key=selected_entry.key,
        name=selected_entry.name,
        type=selected_entry.type,
        value=new_value
    )
    
    # Set the new value
    await registry.set_value(updated_entry)
    console.print(f"[green]Registry value updated: {selected_entry.key}/{selected_entry.name} = {new_value}[/green]")
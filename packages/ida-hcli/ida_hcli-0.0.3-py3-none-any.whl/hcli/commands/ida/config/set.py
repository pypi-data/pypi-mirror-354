from __future__ import annotations
import click
from rich.console import Console
from rich.prompt import Prompt, Confirm

from hcli.lib.commands import async_command
from hcli.lib.registry import Registry, RegistryEntry, RegistryType, string_to_type

console = Console()


@click.command()
@click.option('-k', '--key', default='key', help='Registry key')
@click.option('-t', '--type', 'registry_type', help='One of REG_SZ, REG_DWORD')
@click.argument('name', required=False)
@click.argument('value', required=False)
@async_command
async def set_config(key: str, registry_type: str | None, name: str | None, value: str | None) -> None:
    """Set an IDA registry value."""
    registry = Registry.get_registry()
    
    # Get key from option or prompt
    _key = key or Prompt.ask("Registry key", default="")
    
    # Get name from argument or prompt
    _name = name or Prompt.ask("Setting name", default="")
    
    # Get value from argument or prompt
    _value = value or Prompt.ask("Setting value", default="")
    
    # Get type from option or prompt
    if registry_type:
        try:
            _type = string_to_type(registry_type)
        except ValueError:
            console.print(f"[red]Invalid registry type: {registry_type}[/red]")
            return
    else:
        # Prompt for type selection
        console.print("Select setting type:")
        console.print("1. REG_SZ (string)")
        console.print("2. REG_DWORD (number)")
        
        choice = Prompt.ask("Choose option", choices=["1", "2"], default="1")
        
        if choice == "1":
            _type = RegistryType.REG_SZ
        else:
            _type = RegistryType.REG_DWORD
    
    # Convert value based on type
    if _type == RegistryType.REG_DWORD:
        try:
            converted_value = int(_value)
        except ValueError:
            console.print(f"[red]Invalid number: {_value}[/red]")
            return
    else:
        converted_value = _value
    
    # Create registry entry
    entry = RegistryEntry(
        key=_key,
        name=_name,
        type=_type,
        value=converted_value
    )
    
    await registry.set_value(entry)
    console.print(f"[green]Registry value set: {_key}/{_name} = {converted_value}[/green]")
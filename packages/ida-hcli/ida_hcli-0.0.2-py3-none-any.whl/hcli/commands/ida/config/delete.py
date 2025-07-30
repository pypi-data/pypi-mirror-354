from __future__ import annotations
import click
from rich.console import Console
from rich.prompt import Prompt

from hcli.lib.commands import async_command
from hcli.lib.registry import Registry

console = Console()


@click.command()
@click.option('-k', '--key', help='Registry key')
@click.argument('name', required=False)
@async_command
async def delete_config(key: str | None, name: str | None) -> None:
    """Delete an IDA registry value."""
    registry = Registry.get_registry()
    
    # Get key from option or prompt
    _key = key or Prompt.ask("Registry key", default="")
    
    # Get name from argument or prompt
    _name = name or Prompt.ask("Setting name", default="")
    
    await registry.delete_value(_key, _name)
    console.print(f"Registry {_key}/{_name} deleted")
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
async def get_config(key: str | None, name: str | None) -> None:
    """Get an IDA registry value."""
    registry = Registry.get_registry()
    
    # Get key from option or prompt
    _key = key or Prompt.ask("Registry key", default="")
    
    # Get name from argument or prompt
    _name = name or Prompt.ask("Setting name", default="")
    
    result = await registry.get_value(_key, _name)
    
    if result:
        console.print(f"[green]{result.value}[/green]")
    else:
        console.print(f"[red]Value not found: {_key}/{_name}[/red]")
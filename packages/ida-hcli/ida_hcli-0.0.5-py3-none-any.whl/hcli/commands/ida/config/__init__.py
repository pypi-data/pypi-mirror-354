from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def config() -> None:
    """IDA config commands."""
    pass

from .list import list_config

config.add_command(list_config, name='list')

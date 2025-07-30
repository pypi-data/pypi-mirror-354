from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def group() -> None:
    """Manage plugin groups."""
    pass

from .list import list_groups

group.add_command(list_groups, name='list')

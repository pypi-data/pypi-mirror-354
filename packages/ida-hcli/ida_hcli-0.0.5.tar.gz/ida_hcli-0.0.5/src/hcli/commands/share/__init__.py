from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def share() -> None:
    """Share commands."""
    pass

from .get import get
from .put import put
from .delete import delete
from .list import list_shares

share.add_command(get)
share.add_command(put)
share.add_command(delete)
share.add_command(list_shares, name='list')

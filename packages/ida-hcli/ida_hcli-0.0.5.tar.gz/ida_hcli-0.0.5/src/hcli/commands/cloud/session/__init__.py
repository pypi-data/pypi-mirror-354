from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def session() -> None:
    """Manage cloud analysis sessions."""
    pass

from .list import list_sessions

session.add_command(list_sessions, name='list')

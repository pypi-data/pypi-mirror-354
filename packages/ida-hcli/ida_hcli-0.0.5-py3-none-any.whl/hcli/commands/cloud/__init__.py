from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def cloud() -> None:
    """IDA cloud commands."""
    pass

from .analyze import analyze
from .session import session

cloud.add_command(analyze)
cloud.add_command(session)

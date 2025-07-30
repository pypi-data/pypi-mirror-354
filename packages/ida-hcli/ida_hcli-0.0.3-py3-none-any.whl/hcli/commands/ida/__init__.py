from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def ida() -> None:
    """Manage your IDA installations."""
    pass

from .python import python
from .config import config

ida.add_command(python)
ida.add_command(config)

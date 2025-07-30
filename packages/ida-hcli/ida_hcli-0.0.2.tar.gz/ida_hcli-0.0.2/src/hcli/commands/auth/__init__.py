from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def auth() -> None:
    """Authentication commands."""
    pass

# Subcommands placeholders
from .keys import keys

auth.add_command(keys)

from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.command()
def list_config() -> None:
    console.print("[bold]IDA config list placeholder[/bold]")

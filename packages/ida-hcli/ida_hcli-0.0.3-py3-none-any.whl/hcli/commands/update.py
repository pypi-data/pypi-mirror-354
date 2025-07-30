from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.command()
@click.option('-f', '--force', is_flag=True, help='Force update.')
def update(force: bool) -> None:
    """Update CLI to latest internal version."""
    console.print("[bold]Update placeholder[/bold]")

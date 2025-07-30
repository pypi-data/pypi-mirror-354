from __future__ import annotations
import click
from rich.console import Console
from hcli.commands import register_commands

console = Console()

@click.group()
@click.version_option(package_name="ida-hcli")
def cli():
    """IDA CLI"""
    pass

# register subcommands
register_commands(cli)

if __name__ == "__main__":
    cli()

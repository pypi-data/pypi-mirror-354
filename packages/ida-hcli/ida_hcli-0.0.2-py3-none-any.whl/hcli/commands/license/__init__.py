from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def license() -> None:
    """Manage your licenses."""
    pass

from .list import list_licenses
from .get import get_license
from .install import install_license

license.add_command(list_licenses, name='list')
license.add_command(get_license, name='get')
license.add_command(install_license, name='install')

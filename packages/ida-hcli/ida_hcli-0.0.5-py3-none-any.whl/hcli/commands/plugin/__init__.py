from __future__ import annotations
import click
from rich.console import Console

console = Console()

@click.group()
def plugin() -> None:
    """Manage plugins."""
    pass

from .list import list_plugins
from .install import install
from .uninstall import uninstall
from .update import update_plugin_cmd
from .browse import browse
from .enable import enable
from .group import group
from .search import search
from .submit import submit

plugin.add_command(list_plugins, name='list')
plugin.add_command(install)
plugin.add_command(uninstall)
plugin.add_command(update_plugin_cmd, name='update')
plugin.add_command(browse)
plugin.add_command(enable)
plugin.add_command(group)
plugin.add_command(search)
plugin.add_command(submit)

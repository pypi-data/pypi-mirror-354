from __future__ import annotations
import click


def register_commands(cli: click.Group) -> None:
    """Register all commands to the CLI group."""
    from .login import login
    from .logout import logout
    from .update import update
    from .whoami import whoami
    from .download import download
    from .debug import debug
    # placeholder for more commands

    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(update)
    cli.add_command(whoami)
    cli.add_command(download)
    cli.add_command(debug)

    # groups
    from .auth import auth
    from .cloud import cloud
    from .plugin import plugin
    from .share import share
    from .ida import ida
    from .license import license
    cli.add_command(auth)
    cli.add_command(cloud)
    cli.add_command(plugin)
    cli.add_command(share)
    cli.add_command(ida)
    cli.add_command(license)

from __future__ import annotations

from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Prompt

from hcli.lib.ida import find_standard_installations, get_ida_user_dir, install_license as ida_install_license
from hcli.lib.commands import async_command

console = Console()


@click.command()
@click.argument('file', type=click.Path(exists=True, path_type=Path))
@click.argument('ida_dir', required=False)
@async_command
async def install_license(file: Path, ida_dir: Optional[str]) -> None:
    """Install a license file to an IDA Pro installation directory."""
    # Find IDA installations
    suggested = find_standard_installations()
    user_dir = get_ida_user_dir()
    
    # Build options list
    options = []
    if user_dir:
        options.append(f"1. {user_dir} (user directory)")
    
    for i, installation in enumerate(suggested, len(options) + 1):
        options.append(f"{i}. {installation}")
    
    options.append(f"{len(options) + 1}. Other (specify custom path)")
    
    # Select target directory
    if ida_dir:
        target = ida_dir
    else:
        console.print("\n[bold]Where do you want to install the license?[/bold]")
        for option in options:
            console.print(f"  {option}")
        
        # Get selection
        max_choice = len(options)
        selection = Prompt.ask(
            "Select installation",
            choices=[str(i) for i in range(1, max_choice + 1)],
            default="1" if user_dir else "2" if suggested else "1"
        )
        
        choice_num = int(selection)
        
        if choice_num == 1 and user_dir:
            target = user_dir
        elif choice_num <= len(suggested) + (1 if user_dir else 0):
            # Standard installation
            idx = choice_num - (2 if user_dir else 1)
            target = suggested[idx]
        else:
            # Custom path
            target = Prompt.ask("Enter the target directory path")
    
    # Validate target directory
    target_path = Path(target).expanduser().resolve()
    if not target_path.exists():
        console.print(f"[red]Target directory does not exist: {target_path}[/red]")
        if Prompt.ask("Create directory?", choices=["y", "n"], default="y") == "y":
            target_path.mkdir(parents=True, exist_ok=True)
        else:
            return
    
    try:
        # Install the license
        await ida_install_license(str(file), str(target_path))
        console.print(f"[green]License installed successfully in {target_path}[/green]")
        
        # Show installed file info
        installed_file = target_path / file.name
        if installed_file.exists():
            console.print(f"[dim]License file: {installed_file}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Failed to install license: {e}[/red]")

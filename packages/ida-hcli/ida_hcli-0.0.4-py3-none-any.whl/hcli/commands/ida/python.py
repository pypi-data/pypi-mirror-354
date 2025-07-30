from __future__ import annotations
import asyncio
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.prompt import Prompt

from hcli.lib.commands import async_command
from hcli.lib.registry import Registry, RegistryType, RegistryEntry, KEY_ROOT, PYTHON_TARGET_DLL
from hcli.lib.util.python import get_python_lib, find_python_executables, get_python_lib_for_binary
from hcli.lib.util.io import file_exists

console = Console()


@click.command()
@click.option("-p", "--path", type=str, help="Set python path")
@async_command
async def python(path: Optional[str]) -> None:
    """Set python interpreter for IDA."""
    
    # Get detected Python library
    detected = await get_python_lib()
    
    # Get current python path from registry
    registry = Registry.get_registry()
    current_python_entry = await registry.get_value(KEY_ROOT, PYTHON_TARGET_DLL)
    current_python_path = current_python_entry.value if current_python_entry else None
    
    if current_python_path:
        console.print(f"[blue]Current python interpreter: {current_python_path}[/blue]")
    
    # Determine new Python path
    new_python_path: Optional[str] = None
    
    if path:
        # Use provided path
        new_python_path = path
    else:
        # Interactive selection
        options = []
        default_option = None
        
        # Add detected library as first option
        if detected:
            options.append(f"Detected: {detected}")
            default_option = "1"
        
        # Add current path if different from detected
        if current_python_path and current_python_path != detected:
            options.append(f"Current: {current_python_path}")
            if not default_option:
                default_option = str(len(options))
        
        # Add available Python executables
        executables = await find_python_executables()
        for exe_info in executables:
            display_text = f"Python {exe_info['version']} ({exe_info['binary']})"
            if display_text not in [opt for opt in options]:
                options.append(display_text)
        
        # Add custom option
        options.append("Enter custom path")
        
        if options:
            console.print("\n[bold]Available Python options:[/bold]")
            for i, option in enumerate(options, 1):
                console.print(f"{i}. {option}")
            
            while True:
                choice = Prompt.ask(
                    "Select Python library",
                    choices=[str(i) for i in range(1, len(options) + 1)],
                    default=default_option
                )
                
                choice_idx = int(choice) - 1
                selected_option = options[choice_idx]
                
                if selected_option == "Enter custom path":
                    new_python_path = Prompt.ask("Enter Python library path")
                    break
                elif selected_option.startswith("Detected: "):
                    new_python_path = detected
                    break
                elif selected_option.startswith("Current: "):
                    new_python_path = current_python_path
                    break
                elif selected_option.startswith("Python "):
                    # Extract binary name and get its library
                    binary_name = selected_option.split("(")[1].rstrip(")")
                    console.print(f"[blue]Getting library path for {binary_name}...[/blue]")
                    
                    # Get library for this specific Python
                    try:
                        lib_path = await get_python_lib_for_binary(binary_name)
                        if lib_path:
                            new_python_path = lib_path
                            break
                        else:
                            console.print(f"[yellow]Could not detect library for {binary_name}[/yellow]")
                            new_python_path = Prompt.ask(
                                f"Enter library path for {binary_name}",
                                default=""
                            )
                            break
                    except Exception as e:
                        console.print(f"[red]Could not get library path for {binary_name}: {e}[/red]")
                        continue
                else:
                    break
        else:
            # No options available, prompt for custom path
            default_path = detected or current_python_path or ""
            new_python_path = Prompt.ask(
                "Set python library path",
                default=default_path
            )
    
    # Validate and set the new path
    if new_python_path:
        if file_exists(new_python_path):
            try:
                # Create registry entry
                entry = RegistryEntry(
                    key=KEY_ROOT,
                    name=PYTHON_TARGET_DLL,
                    type=RegistryType.REG_SZ,
                    value=new_python_path
                )
                
                # Set the value
                await registry.set_value(entry)
                
                # Verify the setting was successful
                verification = await registry.get_value(KEY_ROOT, PYTHON_TARGET_DLL)
                if verification and verification.value == new_python_path:
                    console.print(f"[green]Python interpreter set to {new_python_path}[/green]")
                else:
                    console.print(f"[red]Failed to set python interpreter to {new_python_path}[/red]")
                    
            except Exception as e:
                console.print(f"[red]Failed to set python interpreter: {e}[/red]")
        else:
            console.print(f"[red]Invalid path: {new_python_path}[/red]")
    else:
        console.print("[yellow]No python path specified[/yellow]")

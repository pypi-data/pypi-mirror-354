from __future__ import annotations
import os
from pathlib import Path
from typing import Optional, Dict, Any, List

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.tree import Tree

from hcli.lib.api.download import download as download_api, VirtualFileSystem
from hcli.lib.api.common import get_api_client
from hcli.lib.commands import auth_command, async_command

console = Console()


def create_interactive_menu(options: List[Dict[str, Any]], title: str = "Select an option") -> Optional[str]:
    """Create an interactive menu using Rich table and input."""
    if not options:
        console.print("[red]No options available[/red]")
        return None
    
    # Display options in a table
    table = Table(title=title, show_header=True, header_style="bold blue")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Name", style="green")
    
    for i, option in enumerate(options, 1):
        name = option.get("name", str(option))
        table.add_row(str(i), name)
    
    console.print(table)
    
    # Get user input
    while True:
        try:
            choice = Prompt.ask(
                f"Select option (1-{len(options)}) or 'q' to quit",
                default="q"
            )
            
            if choice.lower() == 'q':
                return None
            
            index = int(choice) - 1
            if 0 <= index < len(options):
                selected = options[index]
                return selected.get("value", selected.get("name"))
            else:
                console.print(f"[red]Please enter a number between 1 and {len(options)}[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number or 'q' to quit[/red]")


def traverse_vfs(vfs: VirtualFileSystem, path: str = "", version_filter: str = "") -> Optional[str]:
    """Traverse the virtual file system interactively."""
    current_path = path
    
    while True:
        folders = vfs.get_folders(current_path)
        files = vfs.get_files(current_path)
        
        # Apply version filter if specified
        if version_filter and folders:
            folders = [f for f in folders if version_filter in f]
        
        options = []
        
        # Add navigation options
        if current_path:
            options.append({"name": ".. (Go back)", "value": "back", "type": "navigation"})
        
        # Add folders
        for folder in sorted(folders, reverse=(len(current_path.split("/")) <= 1)):
            options.append({"name": f"📁 {folder}", "value": folder, "type": "folder"})
        
        # Add files
        for file in sorted(files, key=lambda f: f.name):
            display_name = f"📄 {file.name} [{file.id}]"
            options.append({"name": display_name, "value": file.id, "type": "file"})
        
        if not options:
            console.print("[yellow]No items found in this directory[/yellow]")
            if current_path:
                # Go back automatically if no items and we're not at root
                current_path = "/".join(current_path.split("/")[:-1])
                continue
            else:
                return None
        
        # Display current path
        if current_path:
            console.print(f"\n[bold blue]Current path:[/bold blue] {current_path}")
        else:
            console.print(f"\n[bold blue]Browse IDA Downloads[/bold blue]")
        
        choice = create_interactive_menu(options, "Select what to download")
        
        if choice is None:
            return None
        
        if choice == "back":
            # Go back one level
            if current_path:
                parts = current_path.split("/")
                current_path = "/".join(parts[:-1]) if len(parts) > 1 else ""
        else:
            # Check if this is a file (download item)
            selected_option = next((opt for opt in options if opt["value"] == choice), None)
            if selected_option and selected_option["type"] == "file":
                return choice
            elif selected_option and selected_option["type"] == "folder":
                # Navigate into folder
                if current_path:
                    current_path = f"{current_path}/{choice}"
                else:
                    current_path = choice


@auth_command()
@click.option('-f', '--force', is_flag=True, help='Skip cache')
@click.option('--output-dir', 'output_dir', default='./', help='Output path')
@click.option('-v', '--version', 'version_filter', help='Version filter (e.g., 9.1)')
@click.argument('slug', required=False)
@async_command
async def download(force: bool, output_dir: str, version_filter: Optional[str], slug: Optional[str]) -> None:
    """Download IDA binaries, SDK, utilities and more."""
    try:
        # Get downloads from API
        console.print("[yellow]Fetching available downloads...[/yellow]")
        resources = await download_api.get_downloads()
        
        if not resources:
            console.print("[red]No downloads available or unable to fetch downloads[/red]")
            return
        
        console.print(f"[green]Found {len(resources)} available downloads[/green]")
        
        # Create virtual file system
        vfs = VirtualFileSystem(resources)
        
        # If slug is provided, use it directly
        if slug:
            selected_slug = slug
        else:
            # Interactive navigation
            selected_slug = traverse_vfs(vfs, "", version_filter or "")
            
            if not selected_slug:
                console.print("[yellow]Download cancelled[/yellow]")
                return
        
        # Get download URL
        console.print(f"[yellow]Getting download URL for: {selected_slug}[/yellow]")
        try:
            download_url = await download_api.get_download(selected_slug)
        except Exception as e:
            console.print(f"[red]Failed to get download URL: {e}[/red]")
            return
        
        # Download the file
        console.print(f"[yellow]Starting download...[/yellow]")
        client = await get_api_client()
        
        target_path = await client.download_file(
            download_url,
            target_dir=output_dir,
            force=force,
            auth=True
        )
        
        console.print(f"[green]Download complete! File saved to: {target_path}[/green]")
        
    except Exception as e:
        console.print(f"[red]Download failed: {e}[/red]")
        raise

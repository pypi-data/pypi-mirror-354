from __future__ import annotations
import click
from pathlib import Path
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

from hcli.lib.api.share import share, SharedFile
from hcli.lib.api.common import get_api_client
from hcli.lib.commands import async_command, auth_command

console = Console()

@auth_command()
@click.option('--limit', type=int, default=100, 
              help='Maximum number of files to display')
@click.option('--offset', type=int, default=0,
              help='Offset for pagination')
@click.option('--interactive/--no-interactive', default=True,
              help='Enable interactive mode for file operations')
@async_command
async def list_shares(limit: int, offset: int, interactive: bool) -> None:
    """List and manage your shared files."""
    
    try:
        # Get shared files
        with console.status("[bold blue]Loading shared files..."):
            from hcli.lib.api.share import PagingFilter
            filter_params = PagingFilter(limit=limit, offset=offset)
            page = await share.get_files(filter_params)
        
        if not page.items:
            console.print("[yellow]No shared files found.[/yellow]")
            return
        
        # Display files in a table
        display_files_table(page.items)
        
        if interactive:
            await interactive_file_management(page.items)
        
    except Exception as e:
        console.print(f"[red]Error listing files: {e}[/red]")
        raise click.Abort()

def display_files_table(files: List[SharedFile]) -> None:
    """Display files in a formatted table."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Index", style="dim", width=5)
    table.add_column("Code", style="cyan", width=10)
    table.add_column("Name", style="white", width=30)
    table.add_column("Version", style="blue", width=8)
    table.add_column("Size", style="green", width=10)
    table.add_column("Created", style="yellow", width=12)
    table.add_column("ACL", style="red", width=12)
    
    for i, file in enumerate(files, 1):
        name = truncate(file.name or "unnamed", 30)
        version = f"v{file.version}"
        size = format_size(file.size)
        created = format_date(file.created_at) if file.created_at else "N/A"
        acl = file.acl_type
        
        table.add_row(
            str(i),
            file.code,
            name,
            version,
            size,
            created,
            acl
        )
    
    console.print(table)

async def interactive_file_management(files: List[SharedFile]) -> None:
    """Provide interactive file management options."""
    
    while True:
        console.print("\n[bold]File Management Options:[/bold]")
        console.print("1. Download files")
        console.print("2. Delete files") 
        console.print("3. Show file details")
        console.print("4. Exit")
        
        choice = Prompt.ask("Select action", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "4":
            break
        elif choice == "1":
            await download_files_interactive(files)
        elif choice == "2":
            await delete_files_interactive(files)
        elif choice == "3":
            await show_file_details_interactive(files)

async def download_files_interactive(files: List[SharedFile]) -> None:
    """Interactive file download."""
    selected_files = select_files_interactive(files, "Select files to download")
    
    if not selected_files:
        console.print("[yellow]No files selected.[/yellow]")
        return
    
    # Get output directory
    output_dir = Prompt.ask("Output directory", default="./downloads")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Download files
    client = await get_api_client()
    
    for file in selected_files:
        try:
            console.print(f"\n[blue]Downloading {file.name}...[/blue]")
            
            # Get download URL
            file_info = await share.get_file(file.code, file.version)
            
            # Download file
            downloaded_path = await client.download_file(
                file_info.url,
                target_dir=output_path,
                target_filename=file.name,
                force=False,
                auth=True
            )
            
            console.print(f"[green]✓ Downloaded: {downloaded_path}[/green]")
            
        except Exception as e:
            console.print(f"[red]✗ Failed to download {file.name}: {e}[/red]")
    
    console.print(f"\n[green]Download completed. Files saved to: {output_path}[/green]")

async def delete_files_interactive(files: List[SharedFile]) -> None:
    """Interactive file deletion."""
    selected_files = select_files_interactive(files, "Select files to delete")
    
    if not selected_files:
        console.print("[yellow]No files selected.[/yellow]")
        return
    
    # Confirm deletion
    console.print(f"\n[red]You are about to delete {len(selected_files)} file(s):[/red]")
    for file in selected_files:
        console.print(f"  • {file.name} ({file.code})")
    
    if not Confirm.ask("\n[bold red]Are you sure you want to delete these files?[/bold red]"):
        console.print("[yellow]Deletion cancelled.[/yellow]")
        return
    
    # Delete files
    for file in selected_files:
        try:
            await share.delete_file(file.code)
            console.print(f"[green]✓ Deleted: {file.name} ({file.code})[/green]")
        except Exception as e:
            console.print(f"[red]✗ Failed to delete {file.name}: {e}[/red]")

async def show_file_details_interactive(files: List[SharedFile]) -> None:
    """Show detailed information about selected files."""
    selected_files = select_files_interactive(files, "Select files to view details", single_select=True)
    
    if not selected_files:
        console.print("[yellow]No file selected.[/yellow]")
        return
    
    file = selected_files[0]
    
    # Create details panel
    details = Text()
    details.append(f"Name: {file.name or 'unnamed'}\n", style="bold")
    details.append(f"Code: {file.code}\n")
    details.append(f"Version: v{file.version}\n")
    details.append(f"Size: {format_size(file.size)}\n")
    details.append(f"ACL Type: {file.acl_type}\n")
    if file.created_at:
        details.append(f"Created: {format_date(file.created_at)}\n")
    if file.expires_at:
        details.append(f"Expires: {format_date(file.expires_at)}\n")
    details.append(f"URL: {file.url}\n")
    if file.email:
        details.append(f"Owner: {file.email}\n")
    
    panel = Panel(details, title=f"File Details - {file.name}", border_style="blue")
    console.print(panel)

def select_files_interactive(files: List[SharedFile], prompt: str, single_select: bool = False) -> List[SharedFile]:
    """Interactive file selection with multi-select support."""
    
    if single_select:
        console.print(f"\n[bold]{prompt}:[/bold]")
        
        # Display numbered list
        for i, file in enumerate(files, 1):
            name = truncate(file.name or "unnamed", 30)
            console.print(f"  {i}. {name} ({file.code})")
        
        console.print("  0. Cancel")
        
        choices = [str(i) for i in range(len(files) + 1)]
        choice = Prompt.ask("Select file", choices=choices, default="0")
        
        if choice == "0":
            return []
        
        return [files[int(choice) - 1]]
    
    else:
        console.print(f"\n[bold]{prompt}:[/bold]")
        console.print("[dim]Enter comma-separated numbers (e.g., 1,3,5) or ranges (e.g., 1-3,5)[/dim]")
        
        # Display numbered list
        for i, file in enumerate(files, 1):
            name = truncate(file.name or "unnamed", 30)
            console.print(f"  {i}. {name} ({file.code})")
        
        selection = Prompt.ask("Select files", default="")
        
        if not selection.strip():
            return []
        
        try:
            indices = parse_selection(selection, len(files))
            return [files[i-1] for i in indices if 1 <= i <= len(files)]
        except ValueError as e:
            console.print(f"[red]Invalid selection: {e}[/red]")
            return []

def parse_selection(selection: str, max_index: int) -> List[int]:
    """Parse user selection string into list of indices."""
    indices = set()
    
    for part in selection.split(','):
        part = part.strip()
        if '-' in part:
            # Handle range
            start, end = part.split('-', 1)
            start_idx = int(start.strip())
            end_idx = int(end.strip())
            if start_idx > end_idx:
                start_idx, end_idx = end_idx, start_idx
            for i in range(start_idx, end_idx + 1):
                if 1 <= i <= max_index:
                    indices.add(i)
        else:
            # Handle single number
            idx = int(part)
            if 1 <= idx <= max_index:
                indices.add(idx)
    
    return sorted(list(indices))

def format_size(bytes_count: int) -> str:
    """Convert bytes to human-readable format."""
    sizes = ["B", "KB", "MB", "GB", "TB"]
    if bytes_count == 0:
        return "0 B"
    
    import math
    i = int(math.floor(math.log(bytes_count) / math.log(1024)))
    return f"{bytes_count / math.pow(1024, i):.1f} {sizes[i]}"

def format_date(iso_string: str) -> str:
    """Format ISO date string to readable format."""
    from datetime import datetime
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d')
    except:
        return iso_string

def truncate(text: str, max_length: int) -> str:
    """Truncate text with ellipsis if too long."""
    return text[:max_length-3] + "..." if len(text) > max_length else text

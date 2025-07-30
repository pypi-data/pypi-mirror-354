from __future__ import annotations
import asyncio
from datetime import datetime

import click
from rich.console import Console
from rich.table import Table

from hcli.lib.api.cloud import cloud
from hcli.lib.auth import get_auth_service

console = Console()


@click.command()
def list_sessions() -> None:
    """List IDA cloud sessions."""
    asyncio.run(_list_sessions_async())


async def _list_sessions_async() -> None:
    """Async implementation of list sessions command."""
    # Check authentication
    auth_service = get_auth_service()
    if not auth_service.is_logged_in():
        console.print("[red]Error: Not logged in. Please run 'hcli login' first.[/red]")
        return
    
    try:
        sessions = await cloud.get_sessions()
        
        if not sessions:
            console.print("[yellow]No active cloud sessions found.[/yellow]")
            return
        
        table = Table(title="IDA Cloud Sessions")
        table.add_column("Session ID", style="cyan")
        table.add_column("Job ID", style="magenta")
        table.add_column("URL", style="blue")
        table.add_column("Created", style="green")
        table.add_column("Last Activity", style="yellow")
        
        for session in sessions:
            created_time = datetime.fromtimestamp(session.createdAt / 1000).strftime("%Y-%m-%d %H:%M:%S")
            last_activity_time = datetime.fromtimestamp(session.lastActivity / 1000).strftime("%Y-%m-%d %H:%M:%S")
            
            table.add_row(
                session.sessionId,
                session.jobId,
                session.url,
                created_time,
                last_activity_time
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error fetching sessions: {e}[/red]")

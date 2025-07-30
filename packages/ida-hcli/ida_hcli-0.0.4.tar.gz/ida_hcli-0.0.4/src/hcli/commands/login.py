from __future__ import annotations
import click
from rich.console import Console
from rich.prompt import Prompt, Confirm

from hcli.lib.auth import get_auth_service
from hcli.lib.commands import async_command
from hcli.lib.config import config_store

console = Console()

@click.command()
@click.option('-f', '--force', is_flag=True, help='Force account selection.')
@async_command
async def login(force: bool) -> None:
    """Login to hex-rays portal."""
    auth_service = get_auth_service()
    
    # Check if already logged in
    if auth_service.is_logged_in() and not force:
        console.print("[green]You are already logged in.[/green]")
        return
    
    # Get the last used email for suggestions
    current_email = config_store.get_string("login.email", "")
    
    # Choose authentication method
    console.print("\n[bold]How would you like to login?[/bold]")
    console.print("1. Google OAuth")
    console.print("2. Email (OTP)")
    
    while True:
        choice = Prompt.ask("Choose option", choices=["1", "2"], default="1")
        
        if choice == "1":
            # Google OAuth login
            await auth_service.login(force)
            break
        elif choice == "2":
            # Email OTP login
            if current_email:
                email = Prompt.ask("Email address", default=current_email)
            else:
                email = Prompt.ask("Email address")
            
            try:
                console.print(f"[blue]Sending OTP to {email}...[/blue]")
                auth_service.send_otp(email, force)
                
                otp = Prompt.ask("Enter the code received by email")
                
                if auth_service.check_otp(email, otp):
                    config_store.set_string("login.email", email)
                    console.print("[green]Login successful![/green]")
                else:
                    console.print("[red]Login failed. Invalid OTP.[/red]")
            except Exception as e:
                console.print(f"[red]Login failed: {e}[/red]")
            break
    
    # Show login status
    if auth_service.is_logged_in():
        auth_service.show_login_info()

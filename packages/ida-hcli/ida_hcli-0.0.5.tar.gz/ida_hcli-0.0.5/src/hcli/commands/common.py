from __future__ import annotations

from typing import Optional

from rich.console import Console
from rich.prompt import Prompt

from hcli.lib.api.customer import Customer, customer

console = Console()

EXIT_MESSAGES: list[str] = []


def exit_with_messages(code: int = 1) -> None:
    if EXIT_MESSAGES:
        for msg in EXIT_MESSAGES:
            print(msg)
    raise SystemExit(code)


async def select_customer() -> Optional[Customer]:
    """
    Select a customer interactively or return the single customer if only one exists.
    
    Returns:
        Selected customer or None if no customers available
    """
    customers = await customer.get_customers()
    
    if len(customers) > 1:
        console.print("\n[bold]Available customers:[/bold]")
        for i, cust in enumerate(customers, 1):
            name_parts = []
            if cust.first_name:
                name_parts.append(cust.first_name)
            if cust.last_name:
                name_parts.append(cust.last_name)
            if cust.company:
                name_parts.append(f"({cust.company})")
            
            display_name = " ".join(name_parts) if name_parts else cust.email
            console.print(f"  {i}. [{cust.id}] {display_name}")
        
        selection = Prompt.ask(
            "Select customer",
            choices=[str(i) for i in range(1, len(customers) + 1)],
            default="1"
        )
        
        return customers[int(selection) - 1]
        
    elif len(customers) == 1:
        return customers[0]
    else:
        console.print("[red]No customers found[/red]")
        exit_with_messages(1)
        return None

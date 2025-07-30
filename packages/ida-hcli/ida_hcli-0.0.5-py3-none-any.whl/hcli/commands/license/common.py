"""Common license utilities and functions."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional

from rich.console import Console
from rich.prompt import Confirm, Prompt

from hcli.lib.api.license import License, license

console = Console()


async def select_licenses(
    customer_id: str, 
    predicate: Optional[Callable[[License], bool]] = None
) -> List[License]:
    """
    Select licenses interactively or return all matching licenses.
    
    Args:
        customer_id: Customer ID to get licenses for
        predicate: Optional filter function for licenses
        
    Returns:
        List of selected licenses
    """
    if predicate is None:
        predicate = lambda l: True
    
    licenses = await license.get_licenses(customer_id)
    filtered = [l for l in licenses if predicate(l)]
    
    if len(filtered) == 1:
        return filtered
    elif len(filtered) == 0:
        console.print("[yellow]No licenses found matching criteria[/yellow]")
        return []
    else:
        # Group licenses by product catalog
        legacy = [l for l in filtered if l.product_catalog == "legacy"]
        subscription = [l for l in filtered if l.product_catalog == "subscription"]
        
        console.print("\n[bold]Available licenses:[/bold]")
        
        # Display legacy licenses
        if legacy:
            console.print("\n[cyan]Perpetual licenses:[/cyan]")
            for i, lic in enumerate(legacy, 1):
                console.print(f"  {i}. {license_to_string(lic)}")
        
        # Display subscription licenses  
        if subscription:
            console.print("\n[cyan]Subscription licenses:[/cyan]")
            for i, lic in enumerate(subscription, len(legacy) + 1):
                console.print(f"  {i}. {license_to_string(lic)}")
        
        # Simple selection for now - in the future could use a more sophisticated prompt library
        all_licenses = legacy + subscription
        
        console.print(f"\n[bold]Select licenses (comma-separated numbers 1-{len(all_licenses)}, or 'all'):[/bold]")
        selection = Prompt.ask("Selection", default="all")
        
        if selection.lower() == "all":
            return all_licenses
        
        try:
            selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
            selected = [all_licenses[i] for i in selected_indices if 0 <= i < len(all_licenses)]
            return selected
        except (ValueError, IndexError):
            console.print("[red]Invalid selection[/red]")
            return []


async def download_licenses(
    customer_id: str, 
    licenses: List[License], 
    target_dir: str
) -> None:
    """
    Download multiple licenses.
    
    Args:
        customer_id: Customer ID
        licenses: List of licenses to download
        target_dir: Target directory for downloads
    """
    for lic in licenses:
        await download_license(customer_id, lic, target_dir, ask_assets=False)


async def download_license(
    customer_id: str,
    lic: License,
    target_dir: str,
    ask_assets: bool = True,
) -> List[str]:
    """
    Download a single license.
    
    Args:
        customer_id: Customer ID
        lic: License to download
        target_dir: Target directory for downloads
        ask_assets: Whether to ask which asset types to download
        
    Returns:
        List of downloaded file paths
    """
    results = []
    asset_types = lic.asset_types
    
    if not asset_types:
        console.print("[yellow]This license has no assets to download.[/yellow]")
        return results
    
    if ask_assets and len(asset_types) > 0:
        asset_type = asset_types[0]
        if len(asset_types) > 1:
            console.print(f"\n[bold]Available asset types for license {lic.pubhash}:[/bold]")
            for i, asset in enumerate(asset_types, 1):
                console.print(f"  {i}. {asset}")
            
            selection = Prompt.ask(
                "Select asset type",
                choices=[str(i) for i in range(1, len(asset_types) + 1)],
                default="1"
            )
            asset_type = asset_types[int(selection) - 1]
        
        result = await download_license_asset(customer_id, lic, asset_type, target_dir)
        if result:
            results.append(result)
    else:
        # Download all asset types
        for asset_type in asset_types:
            result = await download_license_asset(customer_id, lic, asset_type, target_dir)
            if result:
                results.append(result)
    
    return results


async def download_license_asset(
    customer_id: str,
    lic: License,
    asset_type: str,
    target_dir: str,
) -> Optional[str]:
    """
    Download a specific license asset.
    
    Args:
        customer_id: Customer ID
        lic: License object
        asset_type: Type of asset to download
        target_dir: Target directory for download
        
    Returns:
        Downloaded file path or None if failed
    """
    try:
        filename = await license.download_license(customer_id, lic.pubhash, asset_type, target_dir)
        if filename:
            console.print(f"[green]License {asset_type} for {lic.pubhash} downloaded as: {filename}[/green]")
            return filename
        else:
            console.print("[red]Failed to download license[/red]")
            return None
    except Exception as e:
        console.print(f"[red]Error downloading license: {e}[/red]")
        return None


def license_to_string(lic: License) -> str:
    """
    Convert license object to human-readable string.
    
    Args:
        lic: License object
        
    Returns:
        Formatted license string
    """
    text = "does not expire"
    
    if lic.end_date:
        try:
            end_date = datetime.fromisoformat(lic.end_date.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            if end_date < now:
                # Calculate time since expiration
                delta = now - end_date
                if delta.days > 365:
                    years = delta.days // 365
                    text = f"expired {years} year{'s' if years != 1 else ''} ago"
                elif delta.days > 30:
                    months = delta.days // 30
                    text = f"expired {months} month{'s' if months != 1 else ''} ago"
                elif delta.days > 0:
                    text = f"expired {delta.days} day{'s' if delta.days != 1 else ''} ago"
                else:
                    text = "expired today"
            else:
                # Calculate time until expiration
                delta = end_date - now
                if delta.days > 365:
                    years = delta.days // 365
                    text = f"expires in {years} year{'s' if years != 1 else ''}"
                elif delta.days > 30:
                    months = delta.days // 30
                    text = f"expires in {months} month{'s' if months != 1 else ''}"
                elif delta.days > 0:
                    text = f"expires in {delta.days} day{'s' if delta.days != 1 else ''}"
                else:
                    text = "expires today"
        except (ValueError, TypeError):
            # Fallback if date parsing fails
            text = f"expires {lic.end_date}"
    
    # Get decompilers and other addons
    decompilers = [
        addon.product.code
        for addon in lic.addons
        if addon.product.product_subtype == "DECOMPILER"
    ]
    other = [
        addon.product.code
        for addon in lic.addons
        if addon.product.product_subtype != "DECOMPILER"
    ]
    
    suffix = ""
    if decompilers:
        suffix += f"{len(decompilers)} decompiler{'s' if len(decompilers) != 1 else ''} "
    if other:
        suffix += f"[{', '.join(other)}]"
    
    return f"{lic.pubhash} {lic.edition.edition_name} [{lic.license_type}] {text} {suffix}".strip()


def ensure_target_directory(target_dir: str) -> str:
    """
    Ensure target directory exists and return the absolute path.
    
    Args:
        target_dir: Target directory path
        
    Returns:
        Absolute path to the target directory
    """
    path = Path(target_dir).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return str(path)
"""Version checking utilities."""

from __future__ import annotations
import asyncio
import httpx
from packaging.version import parse, Version
from typing import Optional


async def get_latest_pypi_version(package_name: str) -> Optional[Version]:
    """Get the latest version of a package from PyPI.
    
    Args:
        package_name: Name of the package on PyPI
        
    Returns:
        Latest stable version or None if not found
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            
            data = response.json()
            releases = data.get("releases", {})
            
            latest_stable = parse("0.0.0")
            
            for version_str in releases:
                try:
                    version = parse(version_str)
                    if not version.is_prerelease and version > latest_stable:
                        latest_stable = version
                except Exception:
                    continue
                    
            return latest_stable if latest_stable > parse("0.0.0") else None
            
    except Exception:
        return None


def compare_versions(current: str, latest: Version) -> bool:
    """Compare current version with latest version.
    
    Args:
        current: Current version string
        latest: Latest version from PyPI
        
    Returns:
        True if an update is available
    """
    try:
        current_version = parse(current)
        return latest > current_version
    except Exception:
        return False
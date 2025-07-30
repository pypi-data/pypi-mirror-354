from __future__ import annotations

import os
import platform
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from zlib import crc32


class RegistryType(IntEnum):
    """Registry value types."""
    REG_SZ = 1
    REG_BINARY = 3
    REG_DWORD = 4


@dataclass
class RegistryEntry:
    """Represents a registry entry."""
    key: str
    name: str
    type: RegistryType
    value: Union[int, str, bytes]


class Registry(ABC):
    """Abstract base class for registry operations."""
    
    @abstractmethod
    async def get_values(self) -> List[RegistryEntry]:
        """Get all registry values."""
        pass
    
    @abstractmethod
    async def get_value(self, key: str, name: str) -> Optional[RegistryEntry]:
        """Get a specific registry value."""
        pass
    
    @abstractmethod
    async def delete_value(self, key: str, name: str) -> None:
        """Delete a registry value."""
        pass
    
    @abstractmethod
    async def set_value(self, entry: RegistryEntry) -> None:
        """Set a registry value."""
        pass
    
    @classmethod
    def get_registry(cls, src: Optional[str] = None) -> 'Registry':
        """Get the appropriate registry implementation for the current platform."""
        if platform.system() == "Windows":
            # For now, use FileRegistry on all platforms
            # TODO: Implement WindowsRegistry
            from hcli.lib.ida import get_ida_user_dir
            from hcli.lib.registry.file import FileRegistry
            path = src or os.path.join(get_ida_user_dir() or "", "ida.reg")
            return FileRegistry(path)
        else:
            from hcli.lib.ida import get_ida_user_dir
            from hcli.lib.registry.file import FileRegistry
            path = src or os.path.join(get_ida_user_dir() or "", "ida.reg")
            return FileRegistry(path)


def type_to_string(registry_type: RegistryType) -> str:
    """Convert registry type to string."""
    return {
        RegistryType.REG_SZ: "REG_SZ",
        RegistryType.REG_DWORD: "REG_DWORD", 
        RegistryType.REG_BINARY: "REG_BINARY"
    }.get(registry_type, "UNKNOWN")


def string_to_type(type_str: str) -> RegistryType:
    """Convert string to registry type."""
    mapping = {
        "REG_SZ": RegistryType.REG_SZ,
        "REG_DWORD": RegistryType.REG_DWORD,
        "REG_BINARY": RegistryType.REG_BINARY
    }
    
    if type_str not in mapping:
        raise ValueError(f"Invalid registry type string: {type_str}")
    
    return mapping[type_str]


def value_to_string(entry: RegistryEntry) -> str:
    """Convert registry entry value to string representation."""
    if entry.type == RegistryType.REG_BINARY:
        if not isinstance(entry.value, bytes):
            raise ValueError("Value must be bytes for REG_BINARY")
        return entry.value.hex()
    else:
        return str(entry.value)


# Constants from TypeScript version
KEY_ROOT = ""
PYTHON_TARGET_DLL = "Python3TargetDLL"
DISPLAY_WELCOME = "DisplayWelcome"
EULA_90 = "EULA 90"
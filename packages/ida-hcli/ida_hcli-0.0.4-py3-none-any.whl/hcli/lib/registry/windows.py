"""Windows registry implementation."""

import asyncio
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Union

from hcli.lib.registry import RegistryEntry, Registry, RegistryType, type_to_string, value_to_string

HIVE = "HKEY_CURRENT_USER\\Software\\Hex-Rays\\IDA"


class RegistryValue:
    """Registry value representation."""
    
    def __init__(self, type_: RegistryType, value: Union[str, int, bytes]):
        self.type = type_
        self.value = value


class WindowsRegistry(Registry):
    """Windows registry implementation using reg.exe."""
    
    async def set_value(self, entry: RegistryEntry) -> None:
        """Set a registry value."""
        data = value_to_string(entry)
        key_path = f"{HIVE}{('\\' + entry.key.replace('/', '\\')) if entry.key else ''}"
        
        args = [
            "add",
            key_path,
            "/v",
            f'"{entry.name}"',
            "/t",
            type_to_string(entry.type),
            "/d",
            f'"{data}"',
            "/f",
        ]
        
        await self._run_command(args)
    
    async def get_values(self) -> List[RegistryEntry]:
        """Get all registry values."""
        tree = await self._load_registry()
        entries = []
        
        for key_path, values in tree.items():
            # Extract relative key from full path
            if key_path.startswith(HIVE):
                relative_key = key_path[len(HIVE):].lstrip('\\')
            else:
                relative_key = key_path
            
            for name, reg_value in values.items():
                entries.append(RegistryEntry(
                    relative_key,
                    name,
                    reg_value.type,
                    reg_value.value
                ))
        
        return entries
    
    async def get_value(self, key: str, name: str) -> Optional[RegistryEntry]:
        """Get a specific registry value."""
        try:
            full_key = f"{HIVE}{('\\' + key.replace('/', '\\')) if key else ''}"
            tree = await self._load_registry()
            
            if full_key in tree and name in tree[full_key]:
                reg_value = tree[full_key][name]
                return RegistryEntry(key, name, reg_value.type, reg_value.value)
            
            return None
        except Exception:
            return None
    
    async def delete_value(self, key: str, name: str) -> None:
        """Delete a registry value."""
        key_path = f"{HIVE}\\{key}" if key else HIVE
        args = ["delete", key_path, "/v", f'"{name}"', "/f"]
        await self._run_command(args)
    
    async def _load_registry(self) -> Dict[str, Dict[str, RegistryValue]]:
        """Load registry data by exporting to a temporary file."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.reg', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            await self._run_command(["export", HIVE, tmp_path, "/Y"])
            content = Path(tmp_path).read_text(encoding='utf-16le')
            return self._parse_reg_file(content)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    async def _run_command(self, args: List[str]) -> str:
        """Run a reg.exe command."""
        process = await asyncio.create_subprocess_exec(
            "reg",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode('utf-8', errors='ignore')
            raise RuntimeError(f"Registry command failed: {error_msg}")
        
        return stdout.decode('utf-8', errors='ignore').strip()
    
    def _parse_reg_file(self, content: str) -> Dict[str, Dict[str, RegistryValue]]:
        """Parse a Windows registry export file."""
        lines = content.split('\n')
        registry = {}
        current_key = ""
        last_value_name = None
        last_value_data = []
        
        for line in lines:
            line = line.strip()
            
            if not line or line.startswith("Windows Registry Editor"):
                continue
            
            # Check for key line
            key_match = re.match(r'^\[(.*?)\]$', line)
            if key_match:
                # Save previous value if exists
                if last_value_name and current_key:
                    registry[current_key][last_value_name] = self._parse_value(''.join(last_value_data))
                
                current_key = key_match.group(1)
                registry[current_key] = {}
                last_value_name = None
                last_value_data = []
                continue
            
            # Check for value line
            value_match = re.match(r'^"(.*?)"=(.*)$', line)
            if value_match and current_key:
                # Save previous value if exists
                if last_value_name:
                    registry[current_key][last_value_name] = self._parse_value(''.join(last_value_data))
                
                value_name, value_data = value_match.groups()
                last_value_name = value_name
                last_value_data = [value_data]
                continue
            
            # Handle multi-line hex values
            if last_value_name and line.startswith('  '):
                last_value_data.append(line.strip().rstrip('\\'))
        
        # Save the last value
        if last_value_name and current_key:
            registry[current_key][last_value_name] = self._parse_value(''.join(last_value_data))
        
        return registry
    
    def _parse_value(self, value: str) -> RegistryValue:
        """Parse a registry value from string representation."""
        if value.startswith('dword:'):
            return RegistryValue(RegistryType.REG_DWORD, int(value[6:], 16))
        elif value.startswith('hex:'):
            hex_data = value[4:].replace(',', '')
            return RegistryValue(RegistryType.REG_BINARY, bytes.fromhex(hex_data))
        else:
            # String value - remove quotes and unescape backslashes
            clean_value = value.strip('"').replace('\\\\', '\\')
            return RegistryValue(RegistryType.REG_SZ, clean_value)
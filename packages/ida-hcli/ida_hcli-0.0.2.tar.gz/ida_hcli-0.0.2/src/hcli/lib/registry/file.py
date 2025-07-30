"""File-based registry implementation for non-Windows platforms."""

import struct
from pathlib import Path
from typing import Dict, List, Optional, Union

from hcli.lib.registry import RegistryEntry, Registry, RegistryType
from hcli.lib.util.crc32 import crc32, bytes_to_hex

RCF_SIGNATURE = b"iDa7"


class RegRec:
    """Registry record representation."""
    
    def __init__(self, type_: RegistryType, datalen: int, data: bytes):
        self.type = type_
        self.datalen = datalen
        self.data = data


class RegKey:
    """Registry key representation."""
    
    def __init__(self, name: str):
        self._name = name
        self._entries: Dict[str, Union[RegRec, 'RegKey']] = {}
    
    @property
    def name(self) -> str:
        return self._name
    
    def has(self, key: str) -> bool:
        return key in self._entries
    
    def get(self, key: str) -> Optional[Union[RegRec, 'RegKey']]:
        return self._entries.get(key)
    
    def set(self, key: str, value: Union[RegRec, 'RegKey']) -> None:
        self._entries[key] = value
    
    def delete(self, key: str) -> None:
        if key in self._entries:
            del self._entries[key]
    
    def entries(self):
        return self._entries.items()
    
    def find_key(self, key: str) -> Optional['RegKey']:
        """Find or create a registry key."""
        if not key:
            return self
        
        parts = key.split('\\')
        first_part = parts[0]
        remaining = '\\'.join(parts[1:]) if len(parts) > 1 else ""
        
        key_name = f"\x01{first_part}"
        
        if key_name not in self._entries:
            self._entries[key_name] = RegKey(first_part)
        
        found_key = self._entries[key_name]
        if isinstance(found_key, RegKey):
            if remaining:
                return found_key.find_key(remaining)
            else:
                return found_key
        
        return None
    
    def get_value(self, name: str) -> Optional[RegistryEntry]:
        """Get a registry value as a RegistryEntry."""
        if name not in self._entries:
            return None
        
        rec = self._entries[name]
        if not isinstance(rec, RegRec):
            return None
        
        if rec.type == RegistryType.REG_SZ:
            value = rec.data.decode('utf-8').rstrip('\x00')
            return RegistryEntry(self._name, name, RegistryType.REG_SZ, value)
        elif rec.type == RegistryType.REG_BINARY:
            return RegistryEntry(self._name, name, RegistryType.REG_BINARY, rec.data)
        elif rec.type == RegistryType.REG_DWORD:
            value = struct.unpack('<I', rec.data)[0]
            return RegistryEntry(self._name, name, RegistryType.REG_DWORD, value)
        
        return None


class FileRegistry(Registry):
    """File-based registry implementation."""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    async def delete_value(self, key: str, name: str) -> None:
        """Delete a registry value."""
        root = self._read_root(await self._read_file())
        reg_key = root.find_key(key)
        if reg_key and reg_key.has(name):
            reg_key.delete(name)
            await self._write_file(self._write_tree(root))
    
    async def get_value(self, key: str, name: str) -> Optional[RegistryEntry]:
        """Get a specific registry value."""
        root = self._read_root(await self._read_file())
        reg_key = root.find_key(key)
        if reg_key and reg_key.has(name):
            return reg_key.get_value(name)
        return None
    
    async def get_values(self) -> List[RegistryEntry]:
        """Get all registry values."""
        root = self._read_root(await self._read_file())
        return self._get_values(root)
    
    def _get_values(self, hkey: RegKey) -> List[RegistryEntry]:
        """Recursively get all values from a registry key."""
        entries = []
        for key, value in hkey.entries():
            if isinstance(value, RegKey):
                entries.extend(self._get_values(value))
            else:
                entry = hkey.get_value(key)
                if entry:
                    entries.append(entry)
        return entries
    
    async def set_value(self, entry: RegistryEntry) -> None:
        """Set a registry value."""
        root = self._read_root(await self._read_file())
        reg_key = root.find_key(entry.key)
        
        if reg_key is None:
            raise ValueError(f"Could not find or create key: {entry.key}")
        
        # Convert value to bytes based on type
        if entry.type == RegistryType.REG_SZ:
            data = str(entry.value).encode('utf-8')
        elif entry.type == RegistryType.REG_BINARY:
            data = entry.value if isinstance(entry.value, bytes) else bytes(entry.value)
        elif entry.type == RegistryType.REG_DWORD:
            data = struct.pack('<I', int(entry.value))
        else:
            raise ValueError(f"Unsupported registry type: {entry.type}")
        
        reg_rec = RegRec(entry.type, len(data), data)
        reg_key.set(entry.name, reg_rec)
        await self._write_file(self._write_tree(root))
    
    async def _write_file(self, content: bytes, target: Optional[str] = None) -> None:
        """Write registry content to file with CRC32 checksum."""
        computed_crc_hex = crc32(content, struct.unpack('<I', RCF_SIGNATURE)[0])
        computed_crc = int(computed_crc_hex, 16)
        
        # Write signature + content + CRC
        buffer = bytearray()
        buffer.extend(RCF_SIGNATURE)
        buffer.extend(content)
        buffer.extend(struct.pack('<I', computed_crc))
        
        file_path = Path(target) if target else self.file_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(buffer)
    
    async def _read_file(self) -> bytes:
        """Read and validate registry file."""
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            return b''
        
        data = self.file_path.read_bytes()
        if len(data) < 8:  # Minimum size: signature + CRC
            return b''
        
        # Check signature
        signature = data[:4]
        if signature != RCF_SIGNATURE:
            print(f"Wrong registry signature: {signature}")
            return b''
        
        # Extract content and CRC
        content = data[4:-4]
        file_crc_bytes = data[-4:]
        file_crc = struct.unpack('<I', file_crc_bytes)[0]
        
        # Verify CRC
        computed_crc_hex = crc32(content, struct.unpack('<I', RCF_SIGNATURE)[0])
        computed_crc = int(computed_crc_hex, 16)
        
        if file_crc != computed_crc:
            print(f"CRC mismatch: {file_crc:08x} != {computed_crc:08x}")
        
        return content
    
    def _is_subtree(self, key: str) -> bool:
        """Check if a key represents a subtree."""
        return key.startswith('\x01')
    
    def _read_root(self, buffer: bytes) -> RegKey:
        """Read the root registry key from buffer."""
        root_key = RegKey("")
        if buffer:
            self._read_tree(root_key, buffer, 0)
        return root_key
    
    def _read_tree(self, hkey: RegKey, buffer: bytes, offset: int) -> Optional[int]:
        """Read registry tree from buffer."""
        bad_chars = set(chr(i) for i in range(32))
        
        while offset < len(buffer) and buffer[offset] != 0:
            # Find end of key name
            try:
                end_idx = buffer.index(0, offset)
            except ValueError:
                print("Corrupted registry data")
                return None
            
            if end_idx >= len(buffer):
                print("Corrupted registry data")
                return None
            
            key_len = end_idx - offset
            key_name = ""
            
            # Handle subtree marker
            if buffer[offset] == 1:
                key_name += chr(buffer[offset])
                offset += 1
                key_len -= 1
            
            if key_len == 0 or key_len >= 256:
                print("Corrupted registry data")
                return None
            
            # Read key name
            for i in range(key_len):
                c = chr(buffer[offset])
                if c in bad_chars:
                    print("Corrupted registry data")
                    return None
                key_name += c
                offset += 1
            
            offset += 1  # Skip null terminator
            
            if hkey.has(key_name):
                print("Corrupted registry data")
                return None
            
            if self._is_subtree(key_name):
                # Create subtree
                new_key = RegKey(key_name[1:])
                hkey.set(key_name, new_key)
                offset = self._read_tree(new_key, buffer, offset)
                if offset is None:
                    return None
                offset += 1  # Skip subtree end marker
            else:
                # Read registry record
                if len(buffer) - offset < 5:
                    print("Corrupted registry data")
                    return None
                
                # Read data length (4 bytes, little-endian)
                datalen = struct.unpack('<I', buffer[offset:offset+4])[0]
                offset += 4
                
                # Read type (1 byte)
                type_code = buffer[offset]
                offset += 1
                
                # Validate type
                try:
                    reg_type = RegistryType(type_code)
                except ValueError:
                    print("Corrupted registry data")
                    return None
                
                # Validate data length
                if reg_type == RegistryType.REG_DWORD and datalen != 4:
                    print("Corrupted registry data")
                    return None
                
                if offset + datalen > len(buffer):
                    print("Corrupted registry data")
                    return None
                
                # Read data
                data = buffer[offset:offset + datalen]
                offset += datalen
                
                # Create registry record
                reg_rec = RegRec(reg_type, datalen, data)
                hkey.set(key_name, reg_rec)
        
        return offset
    
    def _write_tree(self, hkey: RegKey) -> bytes:
        """Write registry tree to bytes."""
        output = bytearray()
        self._write_tree_recursive(output, hkey)
        return bytes(output)
    
    def _write_tree_recursive(self, output: bytearray, hkey: RegKey) -> None:
        """Recursively write registry tree."""
        for key, value in hkey.entries():
            # Write key name with null terminator
            key_bytes = key.encode('utf-8') + b'\x00'
            output.extend(key_bytes)
            
            if isinstance(value, RegKey):
                # Write subtree
                self._write_tree_recursive(output, value)
                output.append(0)  # Subtree end marker
            else:
                # Write registry record
                reg_rec = value
                
                # Write data length
                output.extend(struct.pack('<I', reg_rec.datalen))
                
                # Write type
                output.append(reg_rec.type)
                
                # Write data
                output.extend(reg_rec.data)
"""
Binary parsing utilities.

This module provides utilities for reading and writing binary data structures.
"""

import struct
from typing import Optional


class BinaryReader:
    """
    Reader for binary data with multiple encoding support.

    Provides methods for reading various data types from binary data.
    """

    def __init__(self, data: bytes) -> None:
        """
        Initialize the binary reader.

        Args:
            data: Binary data to read from
        """
        self.data = data
        self.offset = 0

    def read_bytes(self, count: int) -> bytes:
        """
        Read a specified number of bytes.

        Args:
            count: Number of bytes to read

        Returns:
            Bytes read from current position

        Raises:
            IndexError: If not enough bytes available
        """
        if self.offset + count > len(self.data):
            raise IndexError(
                f"Cannot read {count} bytes at offset {self.offset} "
                f"(only {len(self.data) - self.offset} bytes remaining)"
            )

        result = self.data[self.offset : self.offset + count]
        self.offset += count
        return result

    def read_byte(self) -> int:
        """
        Read a single byte.

        Returns:
            Byte value (0-255)
        """
        return self.read_bytes(1)[0]

    def read_uint16(self, little_endian: bool = True) -> int:
        """
        Read an unsigned 16-bit integer.

        Args:
            little_endian: Whether to read as little-endian (default True)

        Returns:
            Unsigned 16-bit integer value
        """
        data = self.read_bytes(2)
        fmt = "<H" if little_endian else ">H"
        return struct.unpack(fmt, data)[0]

    def read_uint32(self, little_endian: bool = True) -> int:
        """
        Read an unsigned 32-bit integer.

        Args:
            little_endian: Whether to read as little-endian (default True)

        Returns:
            Unsigned 32-bit integer value
        """
        data = self.read_bytes(4)
        fmt = "<I" if little_endian else ">I"
        return struct.unpack(fmt, data)[0]

    def read_int16(self, little_endian: bool = True) -> int:
        """
        Read a signed 16-bit integer.

        Args:
            little_endian: Whether to read as little-endian (default True)

        Returns:
            Signed 16-bit integer value
        """
        data = self.read_bytes(2)
        fmt = "<h" if little_endian else ">h"
        return struct.unpack(fmt, data)[0]

    def read_int32(self, little_endian: bool = True) -> int:
        """
        Read a signed 32-bit integer.

        Args:
            little_endian: Whether to read as little-endian (default True)

        Returns:
            Signed 32-bit integer value
        """
        data = self.read_bytes(4)
        fmt = "<i" if little_endian else ">i"
        return struct.unpack(fmt, data)[0]

    def read_float(self, little_endian: bool = True) -> float:
        """
        Read a 32-bit floating point number.

        Args:
            little_endian: Whether to read as little-endian (default True)

        Returns:
            Float value
        """
        data = self.read_bytes(4)
        fmt = "<f" if little_endian else ">f"
        return struct.unpack(fmt, data)[0]

    def read_string(self, length: int, encoding: str = "utf-8") -> str:
        """
        Read a string of specified length.

        Args:
            length: Number of bytes to read
            encoding: Text encoding (default 'utf-8')

        Returns:
            Decoded string (null-terminated strings are truncated at null)
        """
        data = self.read_bytes(length)

        # Find null terminator if present
        null_pos = data.find(b"\x00")
        if null_pos != -1:
            data = data[:null_pos]

        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            # Fallback to latin-1 which never fails
            return data.decode("latin-1")

    def read_cstring(self, encoding: str = "utf-8") -> str:
        """
        Read a null-terminated string.

        Args:
            encoding: Text encoding (default 'utf-8')

        Returns:
            Decoded string
        """
        chars = []
        while self.offset < len(self.data):
            byte = self.read_byte()
            if byte == 0:
                break
            chars.append(byte)

        data = bytes(chars)
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            return data.decode("latin-1")

    def skip(self, count: int) -> None:
        """
        Skip a specified number of bytes.

        Args:
            count: Number of bytes to skip
        """
        self.offset += count

    def seek(self, offset: int) -> None:
        """
        Seek to a specific offset.

        Args:
            offset: Offset to seek to
        """
        self.offset = offset

    def tell(self) -> int:
        """
        Get current offset.

        Returns:
            Current offset in bytes
        """
        return self.offset

    def remaining(self) -> int:
        """
        Get number of bytes remaining.

        Returns:
            Number of bytes from current position to end
        """
        return len(self.data) - self.offset


class BinaryWriter:
    """
    Writer for binary data.

    Provides methods for writing various data types to binary format.
    """

    def __init__(self) -> None:
        """Initialize the binary writer."""
        self.data = bytearray()

    def write_bytes(self, data: bytes) -> None:
        """
        Write raw bytes.

        Args:
            data: Bytes to write
        """
        self.data.extend(data)

    def write_byte(self, value: int) -> None:
        """
        Write a single byte.

        Args:
            value: Byte value (0-255)
        """
        self.data.append(value & 0xFF)

    def write_uint16(self, value: int, little_endian: bool = True) -> None:
        """
        Write an unsigned 16-bit integer.

        Args:
            value: Integer value to write
            little_endian: Whether to write as little-endian (default True)
        """
        fmt = "<H" if little_endian else ">H"
        self.data.extend(struct.pack(fmt, value))

    def write_uint32(self, value: int, little_endian: bool = True) -> None:
        """
        Write an unsigned 32-bit integer.

        Args:
            value: Integer value to write
            little_endian: Whether to write as little-endian (default True)
        """
        fmt = "<I" if little_endian else ">I"
        self.data.extend(struct.pack(fmt, value))

    def write_int16(self, value: int, little_endian: bool = True) -> None:
        """
        Write a signed 16-bit integer.

        Args:
            value: Integer value to write
            little_endian: Whether to write as little-endian (default True)
        """
        fmt = "<h" if little_endian else ">h"
        self.data.extend(struct.pack(fmt, value))

    def write_int32(self, value: int, little_endian: bool = True) -> None:
        """
        Write a signed 32-bit integer.

        Args:
            value: Integer value to write
            little_endian: Whether to write as little-endian (default True)
        """
        fmt = "<i" if little_endian else ">i"
        self.data.extend(struct.pack(fmt, value))

    def write_float(self, value: float, little_endian: bool = True) -> None:
        """
        Write a 32-bit floating point number.

        Args:
            value: Float value to write
            little_endian: Whether to write as little-endian (default True)
        """
        fmt = "<f" if little_endian else ">f"
        self.data.extend(struct.pack(fmt, value))

    def write_string(
        self, text: str, length: int, encoding: str = "utf-8", padding: int = 0
    ) -> None:
        """
        Write a string with fixed length.

        Args:
            text: String to write
            length: Fixed length in bytes
            encoding: Text encoding (default 'utf-8')
            padding: Padding byte value (default 0)
        """
        encoded = text.encode(encoding)

        # Truncate if too long
        if len(encoded) > length:
            encoded = encoded[:length]

        # Write string
        self.data.extend(encoded)

        # Pad to length
        if len(encoded) < length:
            self.data.extend(bytes([padding] * (length - len(encoded))))

    def write_cstring(self, text: str, encoding: str = "utf-8") -> None:
        """
        Write a null-terminated string.

        Args:
            text: String to write
            encoding: Text encoding (default 'utf-8')
        """
        encoded = text.encode(encoding)
        self.data.extend(encoded)
        self.data.append(0)  # Null terminator

    def get_bytes(self) -> bytes:
        """
        Get the written bytes.

        Returns:
            Bytes written so far
        """
        return bytes(self.data)

    def clear(self) -> None:
        """Clear all written data."""
        self.data = bytearray()

    def tell(self) -> int:
        """
        Get current write position.

        Returns:
            Current position in bytes
        """
        return len(self.data)

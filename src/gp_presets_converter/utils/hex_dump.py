"""
Hex dump utilities for binary file analysis.

This module provides utilities for creating readable hex dumps of binary data.
"""

from typing import Optional


class HexDumper:
    """
    Utility for creating hex dumps of binary data.

    Provides formatted hex dump output with ASCII representation,
    useful for analyzing binary preset files.
    """

    def __init__(self, bytes_per_line: int = 16) -> None:
        """
        Initialize the hex dumper.

        Args:
            bytes_per_line: Number of bytes to display per line
        """
        self.bytes_per_line = bytes_per_line

    def dump(
        self, data: bytes, offset: int = 0, max_bytes: Optional[int] = None
    ) -> str:
        """
        Create a hex dump of binary data.

        Args:
            data: Binary data to dump
            offset: Starting offset for address display
            max_bytes: Maximum number of bytes to dump (None for all)

        Returns:
            Formatted hex dump as string
        """
        if max_bytes is not None:
            data = data[:max_bytes]

        lines = []
        for i in range(0, len(data), self.bytes_per_line):
            chunk = data[i : i + self.bytes_per_line]
            line = self._format_line(chunk, offset + i)
            lines.append(line)

        return "\n".join(lines)

    def _format_line(self, chunk: bytes, address: int) -> str:
        """
        Format a single line of hex dump.

        Args:
            chunk: Bytes to format
            address: Address to display for this line

        Returns:
            Formatted line string
        """
        # Address column
        addr_str = f"{address:08X}"

        # Hex columns
        hex_parts = []
        for i in range(self.bytes_per_line):
            if i < len(chunk):
                hex_parts.append(f"{chunk[i]:02X}")
            else:
                hex_parts.append("  ")

        # Group hex bytes in pairs
        hex_str = " ".join(hex_parts[i : i + 2] for i in range(0, len(hex_parts), 2))

        # ASCII column
        ascii_str = "".join(self._to_ascii(b) for b in chunk)

        return f"{addr_str}  {hex_str:<{self.bytes_per_line * 2 + (self.bytes_per_line // 2) - 1}}  |{ascii_str}|"

    def _to_ascii(self, byte: int) -> str:
        """
        Convert a byte to printable ASCII character.

        Args:
            byte: Byte value to convert

        Returns:
            ASCII character or '.' if not printable
        """
        if 32 <= byte <= 126:
            return chr(byte)
        return "."

    def dump_comparison(
        self, data1: bytes, data2: bytes, max_bytes: Optional[int] = None
    ) -> str:
        """
        Create a side-by-side hex dump comparison of two binary data sets.

        Args:
            data1: First binary data
            data2: Second binary data
            max_bytes: Maximum number of bytes to dump (None for all)

        Returns:
            Formatted comparison as string
        """
        if max_bytes is not None:
            data1 = data1[:max_bytes]
            data2 = data2[:max_bytes]

        max_len = max(len(data1), len(data2))
        lines = ["=== DATA 1 ===                      === DATA 2 ==="]

        for i in range(0, max_len, self.bytes_per_line):
            chunk1 = data1[i : i + self.bytes_per_line]
            chunk2 = data2[i : i + self.bytes_per_line]

            line1 = self._format_line(chunk1, i) if chunk1 else " " * 70
            line2 = self._format_line(chunk2, i) if chunk2 else " " * 70

            # Highlight differences
            diff_marker = " DIFF" if chunk1 != chunk2 else ""
            lines.append(f"{line1}  {diff_marker}")
            lines.append(f"{line2}  {diff_marker}")
            lines.append("")

        return "\n".join(lines)

    def dump_with_annotations(
        self, data: bytes, annotations: dict[int, str], max_bytes: Optional[int] = None
    ) -> str:
        """
        Create a hex dump with annotations at specific offsets.

        Args:
            data: Binary data to dump
            annotations: Dictionary mapping offsets to annotation strings
            max_bytes: Maximum number of bytes to dump (None for all)

        Returns:
            Formatted hex dump with annotations
        """
        if max_bytes is not None:
            data = data[:max_bytes]

        lines = []
        for i in range(0, len(data), self.bytes_per_line):
            chunk = data[i : i + self.bytes_per_line]
            line = self._format_line(chunk, i)

            # Check if this line has annotations
            line_annotations = []
            for offset in range(i, min(i + self.bytes_per_line, len(data))):
                if offset in annotations:
                    line_annotations.append(f"  @ {offset:04X}: {annotations[offset]}")

            lines.append(line)
            for annotation in line_annotations:
                lines.append(annotation)

        return "\n".join(lines)

    def find_patterns(self, data: bytes, pattern: bytes) -> list[int]:
        """
        Find all occurrences of a pattern in binary data.

        Args:
            data: Binary data to search
            pattern: Pattern to find

        Returns:
            List of offsets where pattern occurs
        """
        offsets = []
        start = 0

        while True:
            pos = data.find(pattern, start)
            if pos == -1:
                break
            offsets.append(pos)
            start = pos + 1

        return offsets

    def dump_around_offset(
        self, data: bytes, offset: int, context_lines: int = 3
    ) -> str:
        """
        Create a hex dump focused on a specific offset with context.

        Args:
            data: Binary data to dump
            offset: Offset to center the dump around
            context_lines: Number of lines of context before and after

        Returns:
            Formatted hex dump
        """
        # Calculate start and end positions
        start = max(0, offset - (context_lines * self.bytes_per_line))
        end = min(len(data), offset + ((context_lines + 1) * self.bytes_per_line))

        # Align start to line boundary
        start = (start // self.bytes_per_line) * self.bytes_per_line

        lines = []
        for i in range(start, end, self.bytes_per_line):
            chunk = data[i : i + self.bytes_per_line]
            line = self._format_line(chunk, i)

            # Mark the line containing the target offset
            if i <= offset < i + self.bytes_per_line:
                line += " <-- TARGET"

            lines.append(line)

        return "\n".join(lines)

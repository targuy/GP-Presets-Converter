"""
Binary file analysis tools.

This module provides utilities for analyzing unknown binary preset files,
including hex dump generation, pattern recognition, and structure detection.
"""

from pathlib import Path
from typing import Dict, List, Tuple, Any

from ..utils.hex_dump import HexDumper
from ..utils.binary_parser import BinaryReader


class BinaryAnalyzer:
    """
    Analyzer for binary preset files.

    Provides tools for exploring and understanding unknown binary file formats,
    including hex dump generation, pattern detection, and structure analysis.
    """

    def __init__(self) -> None:
        """Initialize the binary analyzer."""
        self.hex_dumper = HexDumper()

    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a binary file.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Dictionary containing analysis results

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "rb") as f:
            data = f.read()

        analysis = {
            "file_path": str(file_path),
            "file_size": len(data),
            "signature": self._detect_signature(data),
            "hex_preview": self.hex_dumper.dump(data, max_bytes=256),
            "byte_distribution": self._analyze_byte_distribution(data),
            "possible_strings": self._extract_strings(data),
            "repeating_patterns": self._find_repeating_patterns(data),
            "structure_hints": self._detect_structure(data),
        }

        return analysis

    def _detect_signature(self, data: bytes) -> str:
        """
        Detect file signature from the beginning of data.

        Args:
            data: Binary data to analyze

        Returns:
            Hex representation of file signature (first 16 bytes)
        """
        signature_bytes = data[:16]
        return " ".join(f"{b:02X}" for b in signature_bytes)

    def _analyze_byte_distribution(self, data: bytes) -> Dict[str, Any]:
        """
        Analyze the distribution of byte values in the data.

        Args:
            data: Binary data to analyze

        Returns:
            Dictionary with distribution statistics
        """
        if not data:
            return {"min": 0, "max": 0, "mean": 0, "null_bytes": 0}

        byte_counts = [0] * 256
        for byte in data:
            byte_counts[byte] += 1

        null_bytes = byte_counts[0]
        non_zero = [b for b in data if b != 0]

        return {
            "min": min(non_zero) if non_zero else 0,
            "max": max(non_zero) if non_zero else 0,
            "mean": sum(non_zero) / len(non_zero) if non_zero else 0,
            "null_bytes": null_bytes,
            "null_percentage": (null_bytes / len(data) * 100) if data else 0,
        }

    def _extract_strings(self, data: bytes, min_length: int = 4) -> List[str]:
        """
        Extract printable ASCII strings from binary data.

        Args:
            data: Binary data to analyze
            min_length: Minimum length for extracted strings

        Returns:
            List of extracted strings
        """
        strings = []
        current = []

        for byte in data:
            # Check if byte is printable ASCII
            if 32 <= byte <= 126:
                current.append(chr(byte))
            else:
                if len(current) >= min_length:
                    strings.append("".join(current))
                current = []

        # Add final string if it exists
        if len(current) >= min_length:
            strings.append("".join(current))

        return strings[:20]  # Return first 20 strings

    def _find_repeating_patterns(self, data: bytes, pattern_size: int = 4) -> List[Tuple[bytes, int]]:
        """
        Find repeating byte patterns in the data.

        Args:
            data: Binary data to analyze
            pattern_size: Size of patterns to look for

        Returns:
            List of (pattern, count) tuples for most common patterns
        """
        patterns: Dict[bytes, int] = {}

        for i in range(len(data) - pattern_size + 1):
            pattern = data[i : i + pattern_size]
            patterns[pattern] = patterns.get(pattern, 0) + 1

        # Get top 10 most common patterns (excluding all zeros/all FFs)
        sorted_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)
        filtered = [
            (p, c)
            for p, c in sorted_patterns
            if p not in (b"\x00" * pattern_size, b"\xFF" * pattern_size) and c > 2
        ]

        return filtered[:10]

    def _detect_structure(self, data: bytes) -> Dict[str, Any]:
        """
        Attempt to detect structural elements in the binary data.

        Args:
            data: Binary data to analyze

        Returns:
            Dictionary with detected structural hints
        """
        hints = {
            "header_size_guess": 0,
            "section_boundaries": [],
            "checksum_location_guess": None,
        }

        # Look for null-byte boundaries (common section separators)
        null_runs = []
        in_run = False
        run_start = 0

        for i, byte in enumerate(data):
            if byte == 0:
                if not in_run:
                    in_run = True
                    run_start = i
            else:
                if in_run:
                    if i - run_start >= 4:  # Significant run of nulls
                        null_runs.append((run_start, i))
                    in_run = False

        hints["section_boundaries"] = null_runs[:10]  # First 10 boundaries

        # Guess header size (often 64, 128, 256, or 512 bytes)
        common_header_sizes = [64, 128, 256, 512]
        for size in common_header_sizes:
            if len(data) > size:
                # Check if there's a significant change in byte patterns
                header_section = data[:size]
                body_section = data[size : size + 64] if len(data) > size + 64 else b""
                if body_section and self._sections_differ(header_section, body_section):
                    hints["header_size_guess"] = size
                    break

        return hints

    def _sections_differ(self, section1: bytes, section2: bytes) -> bool:
        """
        Check if two data sections have significantly different characteristics.

        Args:
            section1: First data section
            section2: Second data section

        Returns:
            True if sections appear to differ significantly
        """
        if not section1 or not section2:
            return False

        # Compare null byte percentage
        null1 = section1.count(0) / len(section1)
        null2 = section2.count(0) / len(section2)

        return abs(null1 - null2) > 0.2  # 20% difference threshold

    def compare_files(self, file1: Path, file2: Path) -> Dict[str, Any]:
        """
        Compare two preset files to identify differences.

        Args:
            file1: First file to compare
            file2: Second file to compare

        Returns:
            Dictionary with comparison results
        """
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            data1 = f1.read()
            data2 = f2.read()

        # Find byte-level differences
        differences = []
        min_len = min(len(data1), len(data2))

        for i in range(min_len):
            if data1[i] != data2[i]:
                differences.append(
                    {
                        "offset": i,
                        "file1_value": f"{data1[i]:02X}",
                        "file2_value": f"{data2[i]:02X}",
                    }
                )

        return {
            "file1_size": len(data1),
            "file2_size": len(data2),
            "size_difference": len(data1) - len(data2),
            "byte_differences": len(differences),
            "first_differences": differences[:50],  # Show first 50 differences
            "similarity_percentage": (
                (1 - len(differences) / max(len(data1), len(data2))) * 100
                if max(len(data1), len(data2)) > 0
                else 0
            ),
        }

"""
Preset file parser with hex analysis tools.

This module handles parsing of binary preset files, including header detection,
parameter extraction, and checksum validation for VALETON GP-5 and GP-50
.prst preset file formats.
"""

import struct
from pathlib import Path
from typing import Any, Dict, Optional

from ..models.common import PresetData
from ..utils.binary_parser import BinaryReader


# Real .prst file signatures (5 bytes each)
GP5_PRST_MAGIC = b"GP-5\x00"
GP50_PRST_MAGIC = b"GP-50"

# Legacy test file signatures (from scaffolding)
GP5_LEGACY_SIGNATURE = b"GP5\x00"
GP50_LEGACY_SIGNATURE = b"GP50"


class PresetParser:
    """
    Parser for VALETON preset files with support for multiple formats.

    This parser can handle both GP-5 and GP-50 preset formats (.prst files),
    automatically detecting the format and extracting parameters.
    It also supports legacy test file formats for backwards compatibility.
    """

    # Keep the old attribute names for backwards compatibility with tests
    GP5_SIGNATURE = GP5_LEGACY_SIGNATURE
    GP50_SIGNATURE = GP50_LEGACY_SIGNATURE

    def __init__(self) -> None:
        """Initialize the preset parser."""
        self.format_detected: Optional[str] = None

    def parse_file(self, file_path: Path) -> PresetData:
        """
        Parse a preset file and extract its data.

        Args:
            file_path: Path to the preset file

        Returns:
            PresetData object containing parsed preset information

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not recognized
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Preset file not found: {file_path}")

        with open(file_path, "rb") as f:
            data = f.read()

        # Detect format
        self.format_detected = self._detect_format(data)

        if self.format_detected == "GP5":
            return self._parse_gp5(data)
        elif self.format_detected == "GP50":
            return self._parse_gp50(data)
        elif self.format_detected == "GP5_PRST":
            return self._parse_gp5_prst(data)
        elif self.format_detected == "GP50_PRST":
            return self._parse_gp50_prst(data)
        else:
            return PresetData(
                format="UNKNOWN",
                version="",
                name="Unknown Preset",
                parameters={},
                raw_data=data,
            )

    def _detect_format(self, data: bytes) -> str:
        """
        Detect the preset file format from binary data.

        Args:
            data: Binary data from preset file

        Returns:
            Format string ("GP5", "GP50", "GP5_PRST", "GP50_PRST", or "UNKNOWN")
        """
        if len(data) == 0:
            raise ValueError("Empty preset file")

        # Check for real .prst file signatures first (5 bytes)
        if len(data) >= 5:
            if data[:5] == GP5_PRST_MAGIC:
                return "GP5_PRST"
            elif data[:5] == GP50_PRST_MAGIC:
                return "GP50_PRST"

        # Check for legacy test file signatures (4 bytes)
        if len(data) >= 4:
            if data[:4] == GP5_LEGACY_SIGNATURE:
                return "GP5"
            elif data[:4] == GP50_LEGACY_SIGNATURE:
                return "GP50"

        return "UNKNOWN"

    def _parse_gp5(self, data: bytes) -> PresetData:
        """
        Parse legacy GP-5 format preset data (test file format).

        Args:
            data: Binary data from GP-5 preset file

        Returns:
            PresetData object with GP-5 preset information
        """
        reader = BinaryReader(data)

        # Skip signature
        reader.skip(4)

        # Parse header (legacy placeholder format)
        version = reader.read_string(16)
        name = reader.read_string(32)

        parameters: Dict[str, Any] = {
            "input_gain": 0,
            "output_level": 0,
            "effects_chain": [],
        }

        return PresetData(
            format="GP5",
            version=version.strip(),
            name=name.strip(),
            parameters=parameters,
            raw_data=data,
        )

    def _parse_gp50(self, data: bytes) -> PresetData:
        """
        Parse legacy GP-50 format preset data (test file format).

        Args:
            data: Binary data from GP-50 preset file

        Returns:
            PresetData object with GP-50 preset information
        """
        reader = BinaryReader(data)

        # Skip signature
        reader.skip(4)

        # Parse header (legacy placeholder format)
        version = reader.read_string(16)
        name = reader.read_string(32)

        parameters: Dict[str, Any] = {
            "input_gain": 0,
            "output_level": 0,
            "effects_chain": [],
        }

        return PresetData(
            format="GP50",
            version=version.strip(),
            name=name.strip(),
            parameters=parameters,
            raw_data=data,
        )

    def _parse_gp5_prst(self, data: bytes) -> PresetData:
        """
        Parse a real GP-5 .prst preset file.

        Binary structure:
          0x00-0x04: Magic "GP-5\\x00"
          0x14: Hash byte
          0x15-0x18: FF FF FF FF separator
          0x19-0x28: Preset name (16 bytes, null-padded)
          0x59: Volume parameter value (within 4-byte mixer param)
          0x67-0x74: Amp section (model ID at 0x6D-0x6E)
          0x75-0x7E: Chain order

        Args:
            data: Binary data from GP-5 .prst file

        Returns:
            PresetData object with parsed GP-5 preset information
        """
        # Extract preset name (0x19-0x28, null-terminated)
        name_bytes = data[0x19:0x29]
        null_pos = name_bytes.find(b"\x00")
        if null_pos != -1:
            name_bytes = name_bytes[:null_pos]
        name = name_bytes.decode("ascii", errors="replace")

        # Extract volume (mixer param 1, 4-byte LE at 0x59)
        volume = struct.unpack_from("<I", data, 0x59)[0]

        # Extract amp model ID (2-byte LE at 0x6D)
        amp_model_id = struct.unpack_from("<H", data, 0x6D)[0]

        # Extract chain order (10 bytes at 0x75)
        chain_order = list(data[0x75:0x7F])

        parameters: Dict[str, Any] = {
            "volume": volume,
            "amp_model_id": amp_model_id,
            "chain_order": chain_order,
        }

        return PresetData(
            format="GP5_PRST",
            version="1.0",
            name=name,
            parameters=parameters,
            raw_data=data,
        )

    def _parse_gp50_prst(self, data: bytes) -> PresetData:
        """
        Parse a real GP-50 .prst preset file.

        Binary structure:
          0x00-0x04: Magic "GP-50"
          0x14: Hash byte
          0x15-0x18: FF FF FF FF separator
          0x19-0x28: Preset name (16 bytes, null-padded)
          0x59: Volume parameter value (1-byte mixer param)
          0x92-0x9F: Amp section (model ID at 0x98-0x99)
          0xA0-0xA9: Chain order

        Args:
            data: Binary data from GP-50 .prst file

        Returns:
            PresetData object with parsed GP-50 preset information
        """
        # Extract preset name (0x19-0x28, null-terminated)
        name_bytes = data[0x19:0x29]
        null_pos = name_bytes.find(b"\x00")
        if null_pos != -1:
            name_bytes = name_bytes[:null_pos]
        name = name_bytes.decode("ascii", errors="replace")

        # Extract volume (mixer param 1, 1-byte at 0x59)
        volume = data[0x59]

        # Extract amp model ID (2-byte LE at 0x98)
        amp_model_id = struct.unpack_from("<H", data, 0x98)[0]

        # Extract chain order (10 bytes at 0xA0)
        chain_order = list(data[0xA0:0xAA])

        parameters: Dict[str, Any] = {
            "volume": volume,
            "amp_model_id": amp_model_id,
            "chain_order": chain_order,
        }

        return PresetData(
            format="GP50_PRST",
            version="1.0",
            name=name,
            parameters=parameters,
            raw_data=data,
        )

    def validate_checksum(self, data: bytes) -> bool:
        """
        Validate the checksum of a preset file.

        The checksum algorithm for .prst files has not been fully
        reverse-engineered. This method currently always returns True.

        Args:
            data: Binary data from preset file

        Returns:
            True if checksum is valid (currently always True)
        """
        return True

"""
GP-5 to GP-50 binary conversion logic.

This module handles the core binary conversion between GP-5 and GP-50 .prst
preset formats, based on reverse-engineered binary structure analysis.

Binary format layout (discovered from example preset pairs):

GP5 format (507 bytes):
  0x00-0x04: Magic "GP-5\\x00" (5 bytes)
  0x05-0x13: Metadata/padding (15 bytes)
  0x14:      Hash/identifier byte (1 byte, algorithm unknown)
  0x15-0x28: Name section: FF FF FF FF + name (null-padded, 16 chars) (20 bytes)
  0x29-0x38: Config block (16 bytes, shared between formats)
  0x39-0x3C: Device type "\\x0aEMQ" (4 bytes)
  0x3D-0x52: Post-device config (22 bytes, shared)
  0x53:      Mixer param block length = 0x10 (1 byte)
  0x54:      Mixer header = 0x00 (1 byte)
  0x55-0x66: Mixer params: 2 params in 4-byte format (18 bytes)
  0x67-0x74: Amp section (14 bytes)
  0x75-0x7E: Chain order (10 bytes)
  0x7F:      Chain config (1 byte)
  0x80-0x83: Body marker 30 28 00 1b (4 bytes)
  0x84-0x1EE: FX parameter body (363 bytes)
  0x1EF-0x1FA: Tail (12 bytes: 03 00 08 00 XX 00 00 00 07 00 00 00)

GP50 format (552 bytes):
  0x00-0x04: Magic "GP-50" (5 bytes)
  0x05-0x13: Metadata/padding (15 bytes, same structure)
  0x14:      Hash/identifier byte (1 byte)
  0x15-0x28: Name section (20 bytes, same structure)
  0x29-0x38: Config block (16 bytes, shared)
  0x39-0x3C: Device type "GP50" (4 bytes)
  0x3D-0x52: Post-device config (22 bytes, shared)
  0x53:      Mixer param block length = 0x3B (1 byte)
  0x54:      Mixer header = 0x00 (1 byte)
  0x55-0x91: Mixer params: volume (1-byte) + 9 extra params (61 bytes)
  0x92-0x9F: Amp section (14 bytes)
  0xA0-0xA9: Chain order (10 bytes)
  0xAA:      Chain config (1 byte)
  0xAB-0xAE: Body marker (4 bytes)
  0xAF-0x219: FX parameter body (363 bytes)
  0x21A-0x227: Tail (14 bytes: 03 00 0a 00 XX 00 00 00 YY 00 00 00 ZZ ZZ)
"""

from typing import Any, Dict, List

from ..models.gp5_preset import GP5Preset
from ..models.gp50_preset import GP50Preset


# Binary format constants
GP5_MAGIC = b"GP-5\x00"
GP50_MAGIC = b"GP-50"
GP5_DEVICE_TYPE = b"\x0aEMQ"
GP50_DEVICE_TYPE = b"GP50"
GP5_MIXER_LENGTH = 0x10
GP50_MIXER_LENGTH = 0x3B
GP5_FILE_SIZE = 507
GP50_FILE_SIZE = 552
BODY_MARKER = b"\x30\x28\x00\x1b"

# Default GP50 mixer params 3-10 (added during GP5->GP50 conversion)
GP50_DEFAULT_EXTRA_MIXER = (
    b"\x03\x20\x01\x00\x00"  # param 3: type 0x20, size 1, value 0
    b"\x04\x20\x04\x00\x00\x00\x00\x00"  # param 4: type 0x20, size 4, value 0
    b"\x05\x20\x04\x00\x64\x00\x00\x00"  # param 5: type 0x20, size 4, value 100
    b"\x06\x20\x01\x00\x00"  # param 6: type 0x20, size 1, value 0
    b"\x07\x20\x01\x00\x00"  # param 7: type 0x20, size 1, value 0
    b"\x08\x20\x01\x00\x64"  # param 8: type 0x20, size 1, value 100
    b"\x09\x20\x01\x00\x00"  # param 9: type 0x20, size 1, value 0
    b"\x0a\x20\x01\x00\x00"  # param 10: type 0x20, size 1, value 0
)

# GP50 default footer bytes
GP50_DEFAULT_FOOTER = b"\x05\x05"
# GP5 default tail ending
GP5_DEFAULT_TAIL_END = b"\x07\x00\x00\x00"


class CoreConverter:
    """
    Core binary converter for translating between GP-5 and GP-50 .prst formats.

    Operates directly on the binary data using the reverse-engineered format
    structure discovered from analyzing paired preset examples.
    """

    def __init__(self) -> None:
        """Initialize the core converter."""
        self.conversion_rules = self._load_conversion_rules()

    def _load_conversion_rules(self) -> Dict[str, Any]:
        """
        Load conversion rules for mapping GP-5 parameters to GP-50.

        Returns:
            Dictionary of conversion rules
        """
        return {
            "parameter_mapping": {
                "input_gain": "input_gain",
                "output_level": "output_level",
            },
            "effect_mapping": {
                "overdrive": "overdrive",
                "distortion": "distortion",
                "delay": "delay",
                "reverb": "reverb",
                "chorus": "chorus",
            },
            "parameter_ranges": {
                "input_gain": (0, 100),
                "output_level": (0, 100),
            },
        }

    def convert(self, gp5_preset: GP5Preset) -> GP50Preset:
        """
        Convert a GP-5 preset to GP-50 format (model-based, legacy API).

        Args:
            gp5_preset: GP5Preset object to convert

        Returns:
            GP50Preset object with converted parameters
        """
        converted_params: Dict[str, Any] = {}

        for gp5_key, gp50_key in self.conversion_rules["parameter_mapping"].items():
            if gp5_key in gp5_preset.parameters:
                value = gp5_preset.parameters[gp5_key]
                converted_params[gp50_key] = self._validate_parameter(gp50_key, value)

        converted_effects = []
        for effect in gp5_preset.parameters.get("effects_chain", []):
            if isinstance(effect, dict):
                effect_type = effect.get("type", "")
                if effect_type in self.conversion_rules["effect_mapping"]:
                    converted_effects.append(effect)

        converted_params["effects_chain"] = converted_effects

        gp50_preset = GP50Preset(
            name=gp5_preset.name,
            version="1.0",
            parameters=converted_params,
        )

        return gp50_preset

    def _validate_parameter(self, param_name: str, value: Any) -> Any:
        """Validate and clamp parameter value to valid range."""
        if param_name in self.conversion_rules["parameter_ranges"]:
            min_val, max_val = self.conversion_rules["parameter_ranges"][param_name]
            if isinstance(value, (int, float)):
                return max(min_val, min(max_val, value))
        return value

    def check_compatibility(self, gp5_preset: GP5Preset) -> tuple[bool, list[str]]:
        """Check if a GP-5 preset can be fully converted to GP-50."""
        warnings: list[str] = []
        is_compatible = True

        for effect in gp5_preset.parameters.get("effects_chain", []):
            if isinstance(effect, dict):
                effect_type = effect.get("type", "")
                if effect_type not in self.conversion_rules["effect_mapping"]:
                    warnings.append(f"Effect '{effect_type}' may not be supported in GP-50")
                    is_compatible = False

        return is_compatible, warnings

    # ---- Binary conversion methods (operate on raw .prst bytes) ----

    @staticmethod
    def detect_format(data: bytes) -> str:
        """
        Detect whether binary data is GP5 or GP50 format.

        Supports both real .prst signatures ("GP-5\\x00" / "GP-50") and
        legacy test file signatures ("GP5\\x00" / "GP50").

        Args:
            data: Raw binary preset data

        Returns:
            "GP5" or "GP50"

        Raises:
            ValueError: If format cannot be detected
        """
        if len(data) < 4:
            raise ValueError(f"Data too short ({len(data)} bytes) to detect format")

        # Check real .prst signatures (5 bytes)
        if len(data) >= 5:
            if data[:5] == GP5_MAGIC:
                return "GP5"
            if data[:5] == GP50_MAGIC:
                return "GP50"

        # Check legacy test file signatures (4 bytes)
        if data[:4] == b"GP5\x00":
            return "GP5"
        if data[:4] == b"GP50":
            return "GP50"

        raise ValueError(
            f"Unknown format signature: {data[:5].hex(' ')}"
        )

    @staticmethod
    def convert_gp5_to_gp50(gp5_data: bytes) -> bytes:
        """
        Convert GP-5 binary preset data to GP-50 format.

        The conversion performs these structural transformations:
        1. Changes magic header from "GP-5\\x00" to "GP-50"
        2. Changes device type from "\\x0aEMQ" to "GP50"
        3. Expands mixer section from 2 params (16 bytes) to 10 params (59 bytes)
        4. Changes tail format marker from 0x08 to 0x0a
        5. Adds default values for GP50-specific tail fields
        6. Appends GP50 footer bytes

        Args:
            gp5_data: Raw binary data from a GP-5 .prst file

        Returns:
            Binary data in GP-50 .prst format

        Raises:
            ValueError: If input data is not valid GP-5 format
        """
        if len(gp5_data) != GP5_FILE_SIZE:
            raise ValueError(
                f"Invalid GP5 file size: expected {GP5_FILE_SIZE}, got {len(gp5_data)}"
            )
        if gp5_data[:5] != GP5_MAGIC:
            raise ValueError(
                f"Invalid GP5 magic: expected {GP5_MAGIC.hex()}, got {gp5_data[:5].hex()}"
            )

        result = bytearray()

        # Segment 1: Magic header (5 bytes)
        result.extend(GP50_MAGIC)

        # Segment 2: Metadata (0x05-0x13, 15 bytes) - copy as-is
        result.extend(gp5_data[0x05:0x14])

        # Segment 3: Hash byte (0x14, 1 byte) - preserve original
        # The algorithm is unknown; preserving it is the safest option
        result.append(gp5_data[0x14])

        # Segment 4: Name section (0x15-0x28, 20 bytes) - copy as-is
        result.extend(gp5_data[0x15:0x29])

        # Segment 5: Config block (0x29-0x38, 16 bytes) - copy as-is
        result.extend(gp5_data[0x29:0x39])

        # Segment 6: Device type (4 bytes) - change to GP50
        result.extend(GP50_DEVICE_TYPE)

        # Segment 7: Post-device config (0x3D-0x52, 22 bytes) - copy as-is
        result.extend(gp5_data[0x3D:0x53])

        # Segment 8: Mixer length byte - change to GP50 value
        result.append(GP50_MIXER_LENGTH)

        # Segment 9: Mixer header byte (0x54, 1 byte)
        result.append(gp5_data[0x54])

        # Segment 10: Mixer params - convert from GP5 to GP50 format
        # GP5 param 1: 01 20 04 00 VV 00 00 00 (8 bytes, 4-byte value)
        # GP50 param 1: 01 20 01 00 VV (5 bytes, 1-byte value)
        volume = gp5_data[0x59]  # Extract volume from GP5 4-byte param
        result.extend(b"\x01\x20\x01\x00")
        result.append(volume)

        # GP5 param 2: 02 20 04 00 78 00 00 00 (8 bytes) -> same in GP50
        result.extend(gp5_data[0x5D:0x65])

        # Add GP50-only params 3-10 with default values
        result.extend(GP50_DEFAULT_EXTRA_MIXER)

        # Mixer terminator (2 bytes: 02 00)
        result.extend(gp5_data[0x65:0x67])

        # Segment 11: Amp section (14 bytes) - copy as-is
        result.extend(gp5_data[0x67:0x75])

        # Segment 12: Chain order (10 bytes) - copy as-is
        result.extend(gp5_data[0x75:0x7F])

        # Segment 13: Chain config (1 byte) - copy as-is
        result.append(gp5_data[0x7F])

        # Segment 14: Body marker (4 bytes) - copy as-is
        result.extend(gp5_data[0x80:0x84])

        # Segment 15: FX parameter body (363 bytes) - copy as-is
        result.extend(gp5_data[0x84:0x1EF])

        # Segment 16: Tail - convert format
        # GP5 tail: 03 00 08 00 XX 00 00 00 07 00 00 00
        # GP50 tail: 03 00 0a 00 XX 00 00 00 00 00 00 00 ZZ ZZ
        result.extend(b"\x03\x00")  # Fixed marker
        result.extend(b"\x0a\x00")  # GP50 uses 0x0a (10 mixer params)
        result.extend(gp5_data[0x1F3:0x1F7])  # Copy the config value XX 00 00 00
        result.extend(b"\x00\x00\x00\x00")  # Default for GP50 extra tail field
        result.extend(GP50_DEFAULT_FOOTER)  # GP50 footer

        assert len(result) == GP50_FILE_SIZE, (
            f"Output size mismatch: expected {GP50_FILE_SIZE}, got {len(result)}"
        )

        return bytes(result)

    @staticmethod
    def convert_gp50_to_gp5(gp50_data: bytes) -> bytes:
        """
        Convert GP-50 binary preset data to GP-5 format.

        The conversion performs these structural transformations:
        1. Changes magic header from "GP-50" to "GP-5\\x00"
        2. Changes device type from "GP50" to "\\x0aEMQ"
        3. Compresses mixer section from 10 params to 2 params
        4. Changes tail format marker from 0x0a to 0x08
        5. Removes GP50-specific tail fields and footer

        Args:
            gp50_data: Raw binary data from a GP-50 .prst file

        Returns:
            Binary data in GP-5 .prst format

        Raises:
            ValueError: If input data is not valid GP-50 format
        """
        if len(gp50_data) != GP50_FILE_SIZE:
            raise ValueError(
                f"Invalid GP50 file size: expected {GP50_FILE_SIZE}, got {len(gp50_data)}"
            )
        if gp50_data[:5] != GP50_MAGIC:
            raise ValueError(
                f"Invalid GP50 magic: expected {GP50_MAGIC.hex()}, got {gp50_data[:5].hex()}"
            )

        result = bytearray()

        # Segment 1: Magic header (5 bytes)
        result.extend(GP5_MAGIC)

        # Segment 2: Metadata (0x05-0x13, 15 bytes) - copy as-is
        result.extend(gp50_data[0x05:0x14])

        # Segment 3: Hash byte (0x14, 1 byte) - preserve original
        result.append(gp50_data[0x14])

        # Segment 4: Name section (0x15-0x28, 20 bytes) - copy as-is
        result.extend(gp50_data[0x15:0x29])

        # Segment 5: Config block (0x29-0x38, 16 bytes) - copy as-is
        result.extend(gp50_data[0x29:0x39])

        # Segment 6: Device type (4 bytes) - change to GP5
        result.extend(GP5_DEVICE_TYPE)

        # Segment 7: Post-device config (0x3D-0x52, 22 bytes) - copy as-is
        result.extend(gp50_data[0x3D:0x53])

        # Segment 8: Mixer length byte - change to GP5 value
        result.append(GP5_MIXER_LENGTH)

        # Segment 9: Mixer header byte (0x54, 1 byte)
        result.append(gp50_data[0x54])

        # Segment 10: Mixer params - convert from GP50 to GP5 format
        # GP50 param 1: 01 20 01 00 VV (5 bytes, 1-byte value)
        # GP5 param 1: 01 20 04 00 VV 00 00 00 (8 bytes, 4-byte value)
        volume = gp50_data[0x59]  # Extract volume from GP50 1-byte param
        result.extend(b"\x01\x20\x04\x00")
        result.append(volume)
        result.extend(b"\x00\x00\x00")

        # GP50 param 2: 02 20 04 00 XX 00 00 00 (at offset 0x5A-0x61)
        result.extend(gp50_data[0x5A:0x62])

        # Mixer terminator (2 bytes: 02 00)
        result.extend(gp50_data[0x90:0x92])

        # Skip GP50-only params 3-10 (they are dropped in GP5)

        # Segment 11: Amp section (14 bytes, at GP50 offset 0x92-0x9F)
        result.extend(gp50_data[0x92:0xA0])

        # Segment 12: Chain order (10 bytes, at GP50 offset 0xA0-0xA9)
        result.extend(gp50_data[0xA0:0xAA])

        # Segment 13: Chain config (1 byte, at GP50 offset 0xAA)
        result.append(gp50_data[0xAA])

        # Segment 14: Body marker (4 bytes, at GP50 offset 0xAB-0xAE)
        result.extend(gp50_data[0xAB:0xAF])

        # Segment 15: FX parameter body (363 bytes, at GP50 offset 0xAF-0x219)
        result.extend(gp50_data[0xAF:0x21A])

        # Segment 16: Tail - convert format
        # GP50 tail: 03 00 0a 00 XX 00 00 00 YY 00 00 00 ZZ ZZ
        # GP5 tail:  03 00 08 00 XX 00 00 00 07 00 00 00
        result.extend(b"\x03\x00")  # Fixed marker
        result.extend(b"\x08\x00")  # GP5 uses 0x08
        result.extend(gp50_data[0x21E:0x222])  # Copy config value XX 00 00 00
        result.extend(GP5_DEFAULT_TAIL_END)  # GP5 default ending

        assert len(result) == GP5_FILE_SIZE, (
            f"Output size mismatch: expected {GP5_FILE_SIZE}, got {len(result)}"
        )

        return bytes(result)

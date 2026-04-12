"""
Comprehensive tests for binary GP5 <-> GP50 .prst preset conversion.

Tests conversion using all 10 real preset pairs from the examples directory.
Validates structural correctness, round-trip fidelity, and individual component preservation.
"""

import os
import struct
from pathlib import Path

import pytest

from gp_presets_converter.core.converter import (
    CoreConverter,
    GP5_DEVICE_TYPE,
    GP5_FILE_SIZE,
    GP5_MAGIC,
    GP5_MIXER_LENGTH,
    GP50_DEVICE_TYPE,
    GP50_FILE_SIZE,
    GP50_MAGIC,
    GP50_MIXER_LENGTH,
    BODY_MARKER,
)
from gp_presets_converter.core.parser import PresetParser

# Paths to example preset directories
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
GP5_DIR = EXAMPLES_DIR / "GP5 PRESETS"
GP50_DIR = EXAMPLES_DIR / "GP50 PRESETS"

# Known preset pairs: (GP5 filename, GP50 filename)
PRESET_PAIRS = [
    ("50-80sClean.prst", "55-80sClean.prst"),
    ("51-JazzClean.prst", "56-JazzClean.prst"),
    ("52-Matchless.prst", "57-Matchless.prst"),
    ("53-FunkyRHY.prst", "58-FunkyRhy.prst"),
    ("54-RockRhythm.prst", "59-RockRhythm.prst"),
    ("55-TimPierce.prst", "60-TimPierce.prst"),
    ("56-SLO100.prst", "61-SLO100.prst"),
    ("57-ModernMeta.prst", "62-ModernMeta.prst"),
    ("58-5150.prst", "63-5150.prst"),
    ("59-Lead.prst", "64-LEAD.prst"),
]


def read_file(path: Path) -> bytes:
    """Read a binary file."""
    with open(path, "rb") as f:
        return f.read()


# ---- Fixtures ----


@pytest.fixture
def gp5_files():
    """Return list of all GP5 preset file paths."""
    return [GP5_DIR / name for name, _ in PRESET_PAIRS]


@pytest.fixture
def gp50_files():
    """Return list of all GP50 preset file paths."""
    return [GP50_DIR / name for _, name in PRESET_PAIRS]


# ---- Format Detection Tests ----


class TestFormatDetection:
    """Tests for format detection on real .prst files."""

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_detect_gp5_format(self, gp5_name, _):
        """Verify GP5 format detection for all example files."""
        data = read_file(GP5_DIR / gp5_name)
        assert CoreConverter.detect_format(data) == "GP5"

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_detect_gp50_format(self, _, gp50_name):
        """Verify GP50 format detection for all example files."""
        data = read_file(GP50_DIR / gp50_name)
        assert CoreConverter.detect_format(data) == "GP50"

    def test_detect_invalid_format(self):
        """Verify error on invalid data."""
        with pytest.raises(ValueError, match="Unknown format"):
            CoreConverter.detect_format(b"\x00\x00\x00\x00\x00")

    def test_detect_too_short(self):
        """Verify error on too-short data."""
        with pytest.raises(ValueError, match="too short"):
            CoreConverter.detect_format(b"\x00\x00")


# ---- GP5 File Structure Tests ----


class TestGP5Structure:
    """Verify the discovered GP5 binary structure across all example files."""

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_file_size(self, gp5_name, _):
        """All GP5 files should be exactly 507 bytes."""
        data = read_file(GP5_DIR / gp5_name)
        assert len(data) == GP5_FILE_SIZE

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_magic_header(self, gp5_name, _):
        """All GP5 files should start with 'GP-5\\x00'."""
        data = read_file(GP5_DIR / gp5_name)
        assert data[:5] == GP5_MAGIC

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_device_type(self, gp5_name, _):
        """GP5 device type at 0x39-0x3C should be '\\x0aEMQ'."""
        data = read_file(GP5_DIR / gp5_name)
        assert data[0x39:0x3D] == GP5_DEVICE_TYPE

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_mixer_length(self, gp5_name, _):
        """GP5 mixer length at 0x53 should be 0x10."""
        data = read_file(GP5_DIR / gp5_name)
        assert data[0x53] == GP5_MIXER_LENGTH

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_body_marker(self, gp5_name, _):
        """GP5 body marker at 0x80-0x83 should be 30 28 00 1b."""
        data = read_file(GP5_DIR / gp5_name)
        assert data[0x80:0x84] == BODY_MARKER

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_name_separator(self, gp5_name, _):
        """GP5 name section starts with FF FF FF FF at 0x15."""
        data = read_file(GP5_DIR / gp5_name)
        assert data[0x15:0x19] == b"\xFF\xFF\xFF\xFF"

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_tail_marker(self, gp5_name, _):
        """GP5 tail starts with 03 00 08 00."""
        data = read_file(GP5_DIR / gp5_name)
        assert data[0x1EF:0x1F3] == b"\x03\x00\x08\x00"


# ---- GP50 File Structure Tests ----


class TestGP50Structure:
    """Verify the discovered GP50 binary structure across all example files."""

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_file_size(self, _, gp50_name):
        """All GP50 files should be exactly 552 bytes."""
        data = read_file(GP50_DIR / gp50_name)
        assert len(data) == GP50_FILE_SIZE

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_magic_header(self, _, gp50_name):
        """All GP50 files should start with 'GP-50'."""
        data = read_file(GP50_DIR / gp50_name)
        assert data[:5] == GP50_MAGIC

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_device_type(self, _, gp50_name):
        """GP50 device type at 0x39-0x3C should be 'GP50'."""
        data = read_file(GP50_DIR / gp50_name)
        assert data[0x39:0x3D] == GP50_DEVICE_TYPE

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_mixer_length(self, _, gp50_name):
        """GP50 mixer length at 0x53 should be 0x3B."""
        data = read_file(GP50_DIR / gp50_name)
        assert data[0x53] == GP50_MIXER_LENGTH

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_body_marker(self, _, gp50_name):
        """GP50 body marker at 0xAB-0xAE should be 30 28 00 1b."""
        data = read_file(GP50_DIR / gp50_name)
        assert data[0xAB:0xAF] == BODY_MARKER

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_name_separator(self, _, gp50_name):
        """GP50 name section starts with FF FF FF FF at 0x15."""
        data = read_file(GP50_DIR / gp50_name)
        assert data[0x15:0x19] == b"\xFF\xFF\xFF\xFF"

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_tail_marker(self, _, gp50_name):
        """GP50 tail starts with 03 00 0a 00."""
        data = read_file(GP50_DIR / gp50_name)
        assert data[0x21A:0x21E] == b"\x03\x00\x0a\x00"


# ---- GP5 -> GP50 Conversion Tests ----


class TestGP5ToGP50Conversion:
    """Test GP5 -> GP50 binary conversion with all example presets."""

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_output_size(self, gp5_name, _):
        """Converted GP50 output should be exactly 552 bytes."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        assert len(gp50_data) == GP50_FILE_SIZE

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_magic_header(self, gp5_name, _):
        """Converted output should have GP50 magic header."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        assert gp50_data[:5] == GP50_MAGIC

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_device_type(self, gp5_name, _):
        """Converted output should have GP50 device type."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        assert gp50_data[0x39:0x3D] == GP50_DEVICE_TYPE

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_mixer_length(self, gp5_name, _):
        """Converted output should have GP50 mixer length."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        assert gp50_data[0x53] == GP50_MIXER_LENGTH

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_body_marker(self, gp5_name, _):
        """Converted output should have body marker at GP50 offset."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        assert gp50_data[0xAB:0xAF] == BODY_MARKER

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_name_preserved(self, gp5_name, _):
        """Preset name should be preserved during conversion."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        # Name section is at 0x15-0x28 in both formats
        assert gp5_data[0x15:0x29] == gp50_data[0x15:0x29]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_volume_preserved(self, gp5_name, _):
        """Volume value should be preserved during conversion."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        # GP5 volume: 4-byte LE at 0x59
        gp5_vol = struct.unpack_from("<I", gp5_data, 0x59)[0]
        # GP50 volume: 1-byte at 0x59
        gp50_vol = gp50_data[0x59]
        assert gp5_vol == gp50_vol

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_amp_model_preserved(self, gp5_name, _):
        """Amp model ID should be preserved during conversion."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        # GP5 amp model: 2-byte LE at 0x6D
        gp5_amp = struct.unpack_from("<H", gp5_data, 0x6D)[0]
        # GP50 amp model: 2-byte LE at 0x98
        gp50_amp = struct.unpack_from("<H", gp50_data, 0x98)[0]
        assert gp5_amp == gp50_amp

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_chain_order_preserved(self, gp5_name, _):
        """Chain order should be preserved during conversion."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        # GP5 chain: 0x75-0x7E, GP50 chain: 0xA0-0xA9
        assert gp5_data[0x75:0x7F] == gp50_data[0xA0:0xAA]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_fx_body_preserved(self, gp5_name, _):
        """FX parameter body (363 bytes) should be preserved during conversion."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        # GP5 body: 0x84-0x1EE, GP50 body: 0xAF-0x219
        assert gp5_data[0x84:0x1EF] == gp50_data[0xAF:0x21A]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_config_block_preserved(self, gp5_name, _):
        """Config block (0x29-0x38) should be preserved."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        assert gp5_data[0x29:0x39] == gp50_data[0x29:0x39]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_tail_format(self, gp5_name, _):
        """Converted tail should have GP50 format."""
        gp5_data = read_file(GP5_DIR / gp5_name)
        gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data)
        # Tail starts at 0x21A
        assert gp50_data[0x21A:0x21C] == b"\x03\x00"  # Fixed marker
        assert gp50_data[0x21C:0x21E] == b"\x0a\x00"  # GP50 mixer param count
        # Last 2 bytes should be footer
        assert gp50_data[-2:] == b"\x05\x05"

    def test_invalid_gp5_magic(self):
        """Should raise ValueError for non-GP5 data."""
        fake_data = b"\x00" * GP5_FILE_SIZE
        with pytest.raises(ValueError, match="Invalid GP5 magic"):
            CoreConverter.convert_gp5_to_gp50(fake_data)

    def test_invalid_gp5_size(self):
        """Should raise ValueError for wrong file size."""
        with pytest.raises(ValueError, match="Invalid GP5 file size"):
            CoreConverter.convert_gp5_to_gp50(GP5_MAGIC + b"\x00" * 100)


# ---- GP50 -> GP5 Conversion Tests ----


class TestGP50ToGP5Conversion:
    """Test GP50 -> GP5 binary conversion with all example presets."""

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_output_size(self, _, gp50_name):
        """Converted GP5 output should be exactly 507 bytes."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        assert len(gp5_data) == GP5_FILE_SIZE

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_magic_header(self, _, gp50_name):
        """Converted output should have GP5 magic header."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        assert gp5_data[:5] == GP5_MAGIC

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_device_type(self, _, gp50_name):
        """Converted output should have GP5 device type."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        assert gp5_data[0x39:0x3D] == GP5_DEVICE_TYPE

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_mixer_length(self, _, gp50_name):
        """Converted output should have GP5 mixer length."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        assert gp5_data[0x53] == GP5_MIXER_LENGTH

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_body_marker(self, _, gp50_name):
        """Converted output should have body marker at GP5 offset."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        assert gp5_data[0x80:0x84] == BODY_MARKER

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_name_preserved(self, _, gp50_name):
        """Preset name should be preserved during conversion."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        assert gp50_data[0x15:0x29] == gp5_data[0x15:0x29]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_volume_preserved(self, _, gp50_name):
        """Volume value should be preserved during conversion."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        # GP50 volume: 1-byte at 0x59
        gp50_vol = gp50_data[0x59]
        # GP5 volume: 4-byte LE at 0x59
        gp5_vol = struct.unpack_from("<I", gp5_data, 0x59)[0]
        assert gp50_vol == gp5_vol

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_amp_model_preserved(self, _, gp50_name):
        """Amp model ID should be preserved during conversion."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        # GP50 amp model: 2-byte LE at 0x98
        gp50_amp = struct.unpack_from("<H", gp50_data, 0x98)[0]
        # GP5 amp model: 2-byte LE at 0x6D
        gp5_amp = struct.unpack_from("<H", gp5_data, 0x6D)[0]
        assert gp50_amp == gp5_amp

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_chain_order_preserved(self, _, gp50_name):
        """Chain order should be preserved during conversion."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        # GP50 chain: 0xA0-0xA9, GP5 chain: 0x75-0x7E
        assert gp50_data[0xA0:0xAA] == gp5_data[0x75:0x7F]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_fx_body_preserved(self, _, gp50_name):
        """FX parameter body should be preserved during conversion."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        # GP50 body: 0xAF-0x219, GP5 body: 0x84-0x1EE
        assert gp50_data[0xAF:0x21A] == gp5_data[0x84:0x1EF]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_tail_format(self, _, gp50_name):
        """Converted tail should have GP5 format."""
        gp50_data = read_file(GP50_DIR / gp50_name)
        gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data)
        # GP5 tail starts at 0x1EF
        assert gp5_data[0x1EF:0x1F1] == b"\x03\x00"  # Fixed marker
        assert gp5_data[0x1F1:0x1F3] == b"\x08\x00"  # GP5 mixer param count
        # Last 4 bytes
        assert gp5_data[-4:] == b"\x07\x00\x00\x00"

    def test_invalid_gp50_magic(self):
        """Should raise ValueError for non-GP50 data."""
        fake_data = b"\x00" * GP50_FILE_SIZE
        with pytest.raises(ValueError, match="Invalid GP50 magic"):
            CoreConverter.convert_gp50_to_gp5(fake_data)

    def test_invalid_gp50_size(self):
        """Should raise ValueError for wrong file size."""
        with pytest.raises(ValueError, match="Invalid GP50 file size"):
            CoreConverter.convert_gp50_to_gp5(GP50_MAGIC + b"\x00" * 100)


# ---- Round-Trip Conversion Tests ----


class TestRoundTrip:
    """
    Test round-trip conversion fidelity.

    GP5 -> GP50 -> GP5 should preserve all GP5 data (except the checksum
    byte and tail fields which use defaults in the opposite format).
    GP50 -> GP5 -> GP50 should similarly preserve all GP50 data.
    """

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_structure(self, gp5_name, _):
        """GP5 -> GP50 -> GP5 should produce valid GP5 structure."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)

        # Verify structural correctness
        assert len(roundtrip) == GP5_FILE_SIZE
        assert roundtrip[:5] == GP5_MAGIC
        assert roundtrip[0x39:0x3D] == GP5_DEVICE_TYPE
        assert roundtrip[0x53] == GP5_MIXER_LENGTH
        assert roundtrip[0x80:0x84] == BODY_MARKER

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_name(self, gp5_name, _):
        """Round-trip should preserve preset name exactly."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)
        assert original[0x15:0x29] == roundtrip[0x15:0x29]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_volume(self, gp5_name, _):
        """Round-trip should preserve volume value."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)
        # GP5 volume as 4-byte LE at 0x59
        orig_vol = struct.unpack_from("<I", original, 0x59)[0]
        rt_vol = struct.unpack_from("<I", roundtrip, 0x59)[0]
        assert orig_vol == rt_vol

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_amp_model(self, gp5_name, _):
        """Round-trip should preserve amp model ID."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)
        assert original[0x67:0x75] == roundtrip[0x67:0x75]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_chain_order(self, gp5_name, _):
        """Round-trip should preserve chain order."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)
        assert original[0x75:0x80] == roundtrip[0x75:0x80]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_fx_body(self, gp5_name, _):
        """Round-trip should preserve FX body exactly."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)
        assert original[0x84:0x1EF] == roundtrip[0x84:0x1EF]

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_gp5_roundtrip_metadata(self, gp5_name, _):
        """Round-trip should preserve metadata and config blocks."""
        original = read_file(GP5_DIR / gp5_name)
        intermediate = CoreConverter.convert_gp5_to_gp50(original)
        roundtrip = CoreConverter.convert_gp50_to_gp5(intermediate)
        # Metadata bytes 0x05-0x13
        assert original[0x05:0x14] == roundtrip[0x05:0x14]
        # Hash byte at 0x14
        assert original[0x14] == roundtrip[0x14]
        # Config block 0x29-0x38
        assert original[0x29:0x39] == roundtrip[0x29:0x39]
        # Post-device config 0x3D-0x52
        assert original[0x3D:0x53] == roundtrip[0x3D:0x53]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_gp50_roundtrip_structure(self, _, gp50_name):
        """GP50 -> GP5 -> GP50 should produce valid GP50 structure."""
        original = read_file(GP50_DIR / gp50_name)
        intermediate = CoreConverter.convert_gp50_to_gp5(original)
        roundtrip = CoreConverter.convert_gp5_to_gp50(intermediate)

        # Verify structural correctness
        assert len(roundtrip) == GP50_FILE_SIZE
        assert roundtrip[:5] == GP50_MAGIC
        assert roundtrip[0x39:0x3D] == GP50_DEVICE_TYPE
        assert roundtrip[0x53] == GP50_MIXER_LENGTH
        assert roundtrip[0xAB:0xAF] == BODY_MARKER

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_gp50_roundtrip_name(self, _, gp50_name):
        """Round-trip should preserve preset name exactly."""
        original = read_file(GP50_DIR / gp50_name)
        intermediate = CoreConverter.convert_gp50_to_gp5(original)
        roundtrip = CoreConverter.convert_gp5_to_gp50(intermediate)
        assert original[0x15:0x29] == roundtrip[0x15:0x29]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_gp50_roundtrip_volume(self, _, gp50_name):
        """Round-trip should preserve volume value."""
        original = read_file(GP50_DIR / gp50_name)
        intermediate = CoreConverter.convert_gp50_to_gp5(original)
        roundtrip = CoreConverter.convert_gp5_to_gp50(intermediate)
        assert original[0x59] == roundtrip[0x59]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_gp50_roundtrip_amp_model(self, _, gp50_name):
        """Round-trip should preserve amp model ID."""
        original = read_file(GP50_DIR / gp50_name)
        intermediate = CoreConverter.convert_gp50_to_gp5(original)
        roundtrip = CoreConverter.convert_gp5_to_gp50(intermediate)
        assert original[0x92:0xA0] == roundtrip[0x92:0xA0]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_gp50_roundtrip_chain_order(self, _, gp50_name):
        """Round-trip should preserve chain order."""
        original = read_file(GP50_DIR / gp50_name)
        intermediate = CoreConverter.convert_gp50_to_gp5(original)
        roundtrip = CoreConverter.convert_gp5_to_gp50(intermediate)
        assert original[0xA0:0xAB] == roundtrip[0xA0:0xAB]

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_gp50_roundtrip_fx_body(self, _, gp50_name):
        """Round-trip should preserve FX body exactly."""
        original = read_file(GP50_DIR / gp50_name)
        intermediate = CoreConverter.convert_gp50_to_gp5(original)
        roundtrip = CoreConverter.convert_gp5_to_gp50(intermediate)
        assert original[0xAF:0x21A] == roundtrip[0xAF:0x21A]


# ---- Parser Tests ----


class TestParserWithRealFiles:
    """Test the PresetParser with real .prst files."""

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_parse_gp5_prst(self, gp5_name, _):
        """Parser should correctly detect and parse GP5 .prst files."""
        parser = PresetParser()
        data = parser.parse_file(GP5_DIR / gp5_name)
        assert data.format == "GP5_PRST"
        assert data.name != ""
        assert "volume" in data.parameters
        assert "amp_model_id" in data.parameters
        assert "chain_order" in data.parameters

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_parse_gp50_prst(self, _, gp50_name):
        """Parser should correctly detect and parse GP50 .prst files."""
        parser = PresetParser()
        data = parser.parse_file(GP50_DIR / gp50_name)
        assert data.format == "GP50_PRST"
        assert data.name != ""
        assert "volume" in data.parameters
        assert "amp_model_id" in data.parameters
        assert "chain_order" in data.parameters

    def test_parse_gp5_preset_names(self):
        """Verify parsed preset names match expected values."""
        parser = PresetParser()
        expected_names = {
            "50-80sClean.prst": "80s Clean",
            "51-JazzClean.prst": "Jazz Clean",
            "52-Matchless.prst": "Matchless",
            "55-TimPierce.prst": "TimPierce",
            "58-5150.prst": "5150",
            "59-Lead.prst": "Lead",
        }
        for filename, expected_name in expected_names.items():
            data = parser.parse_file(GP5_DIR / filename)
            assert data.name == expected_name, f"Name mismatch for {filename}"


# ---- File-Level Converter Tests ----


class TestPresetConverterWithFiles:
    """Test the PresetConverter class with real .prst files."""

    @pytest.mark.parametrize("gp5_name,_", PRESET_PAIRS)
    def test_convert_gp5_file(self, gp5_name, _, tmp_path):
        """Convert a GP5 .prst file to GP50 using PresetConverter."""
        from gp_presets_converter import PresetConverter

        converter = PresetConverter()
        output = tmp_path / "output.prst"
        result = converter.convert_file(GP5_DIR / gp5_name, output)

        assert result.exists()
        data = read_file(result)
        assert len(data) == GP50_FILE_SIZE
        assert data[:5] == GP50_MAGIC

    @pytest.mark.parametrize("_,gp50_name", PRESET_PAIRS)
    def test_convert_gp50_file(self, _, gp50_name, tmp_path):
        """Convert a GP50 .prst file to GP5 using PresetConverter."""
        from gp_presets_converter import PresetConverter

        converter = PresetConverter()
        output = tmp_path / "output.prst"
        result = converter.convert_file(GP50_DIR / gp50_name, output)

        assert result.exists()
        data = read_file(result)
        assert len(data) == GP5_FILE_SIZE
        assert data[:5] == GP5_MAGIC

    def test_batch_convert_gp5_directory(self, tmp_path):
        """Convert an entire GP5 directory to GP50."""
        from gp_presets_converter import PresetConverter

        converter = PresetConverter()
        output_dir = tmp_path / "gp50_output"
        results = converter.convert_directory(GP5_DIR, output_dir, "GP50")

        assert len(results) == 10
        for result in results:
            assert result.exists()
            data = read_file(result)
            assert len(data) == GP50_FILE_SIZE

    def test_batch_convert_gp50_directory(self, tmp_path):
        """Convert an entire GP50 directory to GP5."""
        from gp_presets_converter import PresetConverter

        converter = PresetConverter()
        output_dir = tmp_path / "gp5_output"
        results = converter.convert_directory(GP50_DIR, output_dir, "GP5")

        assert len(results) == 10
        for result in results:
            assert result.exists()
            data = read_file(result)
            assert len(data) == GP5_FILE_SIZE

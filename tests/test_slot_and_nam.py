"""
Tests for slot renaming and NAM/SnapTone remapping features.

Covers:
- Filename slot parsing and replacement helpers
- NAM reference reading from real .prst files
- NAM remapping during GP5<->GP50 binary conversion
- File-level slot conversion (convert_file with target_slot)
- Directory batch slot conversion (convert_directory with start_slot)
"""

import shutil
from pathlib import Path

import pytest

from gp_presets_converter.converter import (
    PresetConverter,
    _parse_slot_from_filename,
    _replace_slot_in_filename,
)
from gp_presets_converter.core.converter import (
    CoreConverter,
    GP5_NAM_REF_OFFSET,
    GP50_NAM_REF_OFFSET,
)

# Paths to real example presets
EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
GP5_DIR = EXAMPLES_DIR / "GP5 PRESETS"
GP50_DIR = EXAMPLES_DIR / "GP50 PRESETS"


# ---------------------------------------------------------------------------
# 1. Filename slot parsing
# ---------------------------------------------------------------------------
class TestParseSlotFromFilename:
    """Tests for _parse_slot_from_filename helper."""

    def test_parse_standard_slot(self):
        assert _parse_slot_from_filename("55-TimPierce.prst") == 55

    def test_parse_zero_slot(self):
        assert _parse_slot_from_filename("0-Preset.prst") == 0

    def test_parse_high_slot(self):
        assert _parse_slot_from_filename("127-Preset.prst") == 127

    def test_no_slot_prefix(self):
        assert _parse_slot_from_filename("myPreset.prst") is None

    def test_no_dash_separator(self):
        assert _parse_slot_from_filename("Preset.prst") is None

    def test_parse_without_extension(self):
        assert _parse_slot_from_filename("50-80sClean") == 50

    def test_parse_multi_digit(self):
        assert _parse_slot_from_filename("100-Name.prst") == 100


# ---------------------------------------------------------------------------
# 2. Filename slot replacement
# ---------------------------------------------------------------------------
class TestReplaceSlotInFilename:
    """Tests for _replace_slot_in_filename helper."""

    def test_replace_existing_slot(self):
        assert _replace_slot_in_filename("55-TimPierce.prst", 70) == "70-TimPierce.prst"

    def test_prepend_slot_when_missing(self):
        assert _replace_slot_in_filename("myPreset.prst", 70) == "70-myPreset.prst"

    def test_replace_zero_slot(self):
        assert _replace_slot_in_filename("0-Preset.prst", 5) == "5-Preset.prst"

    def test_replace_preserves_extension(self):
        result = _replace_slot_in_filename("50-80sClean.prst", 99)
        assert result.endswith(".prst")
        assert result.startswith("99-")


# ---------------------------------------------------------------------------
# 3. NAM reference reading from real files
# ---------------------------------------------------------------------------
class TestGetNamRef:
    """Tests for CoreConverter.get_nam_ref on real example presets."""

    def test_gp5_80sclean_nam_ref(self):
        data = (GP5_DIR / "50-80sClean.prst").read_bytes()
        assert CoreConverter.get_nam_ref(data) == 50

    def test_gp50_80sclean_nam_ref(self):
        data = (GP50_DIR / "55-80sClean.prst").read_bytes()
        assert CoreConverter.get_nam_ref(data) == 50

    def test_gp5_timpierce_no_nam(self):
        data = (GP5_DIR / "55-TimPierce.prst").read_bytes()
        assert CoreConverter.get_nam_ref(data) == 0

    def test_raw_offset_gp5(self):
        """Verify the constant offset directly."""
        data = (GP5_DIR / "50-80sClean.prst").read_bytes()
        assert data[GP5_NAM_REF_OFFSET] == 50

    def test_raw_offset_gp50(self):
        """Verify the constant offset directly."""
        data = (GP50_DIR / "55-80sClean.prst").read_bytes()
        assert data[GP50_NAM_REF_OFFSET] == 50


# ---------------------------------------------------------------------------
# 4. NAM remapping – GP5 -> GP50
# ---------------------------------------------------------------------------
class TestNamRemapGp5ToGp50:
    """Tests for NAM offset remapping during convert_gp5_to_gp50."""

    @pytest.fixture()
    def gp5_80sclean(self):
        return (GP5_DIR / "50-80sClean.prst").read_bytes()

    @pytest.fixture()
    def gp5_timpierce(self):
        return (GP5_DIR / "55-TimPierce.prst").read_bytes()

    def test_positive_offset(self, gp5_80sclean):
        result = CoreConverter.convert_gp5_to_gp50(gp5_80sclean, nam_offset=5)
        assert result[GP50_NAM_REF_OFFSET] == 55

    def test_negative_offset(self, gp5_80sclean):
        result = CoreConverter.convert_gp5_to_gp50(gp5_80sclean, nam_offset=-3)
        assert result[GP50_NAM_REF_OFFSET] == 47

    def test_zero_offset_unchanged(self, gp5_80sclean):
        result = CoreConverter.convert_gp5_to_gp50(gp5_80sclean, nam_offset=0)
        assert result[GP50_NAM_REF_OFFSET] == 50

    def test_no_nam_stays_zero(self, gp5_timpierce):
        """NAM ref 0 (no NAM) must stay 0 regardless of offset."""
        result = CoreConverter.convert_gp5_to_gp50(gp5_timpierce, nam_offset=5)
        assert result[GP50_NAM_REF_OFFSET] == 0

    def test_out_of_range_raises(self, gp5_80sclean):
        """Remapping below 1 should raise ValueError."""
        with pytest.raises(ValueError, match="out of range"):
            CoreConverter.convert_gp5_to_gp50(gp5_80sclean, nam_offset=-50)

    def test_out_of_range_high_raises(self, gp5_80sclean):
        """Remapping above 255 should raise ValueError."""
        with pytest.raises(ValueError, match="out of range"):
            CoreConverter.convert_gp5_to_gp50(gp5_80sclean, nam_offset=206)


# ---------------------------------------------------------------------------
# 5. NAM remapping – GP50 -> GP5
# ---------------------------------------------------------------------------
class TestNamRemapGp50ToGp5:
    """Tests for NAM offset remapping during convert_gp50_to_gp5."""

    @pytest.fixture()
    def gp50_80sclean(self):
        return (GP50_DIR / "55-80sClean.prst").read_bytes()

    @pytest.fixture()
    def gp50_timpierce(self):
        return (GP50_DIR / "60-TimPierce.prst").read_bytes()

    def test_positive_offset(self, gp50_80sclean):
        result = CoreConverter.convert_gp50_to_gp5(gp50_80sclean, nam_offset=5)
        assert result[GP5_NAM_REF_OFFSET] == 55

    def test_negative_offset(self, gp50_80sclean):
        result = CoreConverter.convert_gp50_to_gp5(gp50_80sclean, nam_offset=-3)
        assert result[GP5_NAM_REF_OFFSET] == 47

    def test_zero_offset_unchanged(self, gp50_80sclean):
        result = CoreConverter.convert_gp50_to_gp5(gp50_80sclean, nam_offset=0)
        assert result[GP5_NAM_REF_OFFSET] == 50

    def test_no_nam_stays_zero_gp50_to_gp5(self, gp50_timpierce):
        """
        GP50 TimPierce has NAM ref 55 (not 0), so use a file we know has 0.
        Build one synthetically by zeroing the NAM ref in a copy.
        """
        buf = bytearray(gp50_timpierce)
        buf[GP50_NAM_REF_OFFSET] = 0
        result = CoreConverter.convert_gp50_to_gp5(bytes(buf), nam_offset=10)
        assert result[GP5_NAM_REF_OFFSET] == 0

    def test_out_of_range_raises(self, gp50_80sclean):
        with pytest.raises(ValueError, match="out of range"):
            CoreConverter.convert_gp50_to_gp5(gp50_80sclean, nam_offset=-50)

    def test_out_of_range_high_raises(self, gp50_80sclean):
        with pytest.raises(ValueError, match="out of range"):
            CoreConverter.convert_gp50_to_gp5(gp50_80sclean, nam_offset=206)


# ---------------------------------------------------------------------------
# 6. File-level slot conversion (PresetConverter.convert_file)
# ---------------------------------------------------------------------------
class TestConvertFileSlot:
    """Tests for PresetConverter.convert_file with target_slot."""

    @pytest.fixture()
    def converter(self):
        return PresetConverter()

    def test_target_slot_in_output_filename(self, converter, tmp_path):
        src = GP5_DIR / "50-80sClean.prst"
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        out_path = out_dir / src.name

        result = converter.convert_file(src, out_path, target_slot=70)
        assert result.name.startswith("70-")
        assert result.exists()

    def test_none_slot_preserves_original(self, converter, tmp_path):
        src = GP5_DIR / "50-80sClean.prst"
        out_dir = tmp_path / "out"
        out_dir.mkdir()
        out_path = out_dir / src.name

        result = converter.convert_file(src, out_path, target_slot=None)
        # No slot renaming; output should keep the name provided by out_path
        assert result.name == src.name
        assert result.exists()

    def test_target_slot_negative_raises(self, converter, tmp_path):
        src = GP5_DIR / "50-80sClean.prst"
        with pytest.raises(ValueError):
            converter.convert_file(src, target_slot=-1)

    def test_target_slot_128_raises(self, converter, tmp_path):
        src = GP5_DIR / "50-80sClean.prst"
        with pytest.raises(ValueError):
            converter.convert_file(src, target_slot=128)

    def test_auto_output_with_target_slot(self, converter, tmp_path):
        """When output_path is None, the converter generates one with the slot."""
        src_copy = tmp_path / "50-80sClean.prst"
        shutil.copy2(GP5_DIR / "50-80sClean.prst", src_copy)

        result = converter.convert_file(src_copy, target_slot=70)
        assert "70-" in result.name
        assert result.exists()


# ---------------------------------------------------------------------------
# 7. Directory batch slot conversion (PresetConverter.convert_directory)
# ---------------------------------------------------------------------------
class TestConvertDirectorySlot:
    """Tests for PresetConverter.convert_directory with start_slot."""

    @pytest.fixture()
    def converter(self):
        return PresetConverter()

    @pytest.fixture()
    def three_gp5_files(self, tmp_path):
        """Copy 3 GP5 preset files into a temp directory."""
        src_dir = tmp_path / "input"
        src_dir.mkdir()
        files = sorted(GP5_DIR.glob("*.prst"))[:3]
        for f in files:
            shutil.copy2(f, src_dir / f.name)
        return src_dir

    def test_start_slot_renumbers_output(self, converter, tmp_path, three_gp5_files):
        out_dir = tmp_path / "output"
        results = converter.convert_directory(
            three_gp5_files, out_dir, start_slot=80,
        )
        assert len(results) == 3
        names = sorted(r.name for r in results)
        for i, name in enumerate(names):
            assert name.startswith(f"{80 + i}-"), f"Expected slot {80+i} in {name}"
        # NAM refs should be unchanged (no nam_offset applied)
        # Original GP5 files have NAM refs 50, 51, 52 respectively
        original_nams = [50, 51, 52]
        for result_path, expected_nam in zip(sorted(results, key=lambda p: p.name), original_nams):
            data = result_path.read_bytes()
            nam = CoreConverter.get_nam_ref(data)
            assert nam == expected_nam, f"{result_path.name}: expected NAM {expected_nam}, got {nam}"

    def test_start_slot_none_keeps_original(self, converter, tmp_path, three_gp5_files):
        out_dir = tmp_path / "output"
        results = converter.convert_directory(
            three_gp5_files, out_dir, start_slot=None,
        )
        assert len(results) == 3
        # Original filenames should be preserved (no renumbering)
        original_names = sorted(f.name for f in three_gp5_files.glob("*.prst"))
        result_names = sorted(r.name for r in results)
        assert result_names == original_names

    def test_directory_with_nam_offset(self, converter, tmp_path, three_gp5_files):
        """Batch conversion with nam_offset applies to every file."""
        out_dir = tmp_path / "output"
        results = converter.convert_directory(
            three_gp5_files, out_dir, nam_offset=5,
        )
        # Verify at least one output has the remapped NAM ref
        for result_path in results:
            data = result_path.read_bytes()
            nam = CoreConverter.get_nam_ref(data)
            # Original NAM was 50 for 80sClean; if it had a NAM, it should be shifted
            # Files with NAM ref 0 stay 0
            if nam > 0:
                assert nam != 50, "NAM ref should have been shifted by +5"

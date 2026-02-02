"""
Unit tests for utility modules.
"""

import pytest
from pathlib import Path

from gp_presets_converter.utils import (
    BinaryReader,
    BinaryWriter,
    FileHandler,
    HexDumper,
    PresetValidator
)


@pytest.mark.unit
class TestBinaryReader:
    """Test cases for BinaryReader."""

    def test_read_bytes(self):
        """Test reading raw bytes."""
        data = b'\x01\x02\x03\x04\x05'
        reader = BinaryReader(data)

        result = reader.read_bytes(3)
        assert result == b'\x01\x02\x03'
        assert reader.tell() == 3

    def test_read_byte(self):
        """Test reading single byte."""
        data = b'\xFF\x00\x42'
        reader = BinaryReader(data)

        assert reader.read_byte() == 0xFF
        assert reader.read_byte() == 0x00
        assert reader.read_byte() == 0x42

    def test_read_uint16_little_endian(self):
        """Test reading 16-bit unsigned integer (little endian)."""
        data = b'\x01\x02'
        reader = BinaryReader(data)

        result = reader.read_uint16(little_endian=True)
        assert result == 0x0201  # Little endian: 0x02 * 256 + 0x01

    def test_read_string(self):
        """Test reading fixed-length string."""
        data = b'Hello\x00\x00\x00World'
        reader = BinaryReader(data)

        result = reader.read_string(8)
        assert result == "Hello"  # Null-terminated

    def test_skip_and_seek(self):
        """Test skip and seek operations."""
        data = b'\x00\x01\x02\x03\x04'
        reader = BinaryReader(data)

        reader.skip(2)
        assert reader.tell() == 2

        reader.seek(0)
        assert reader.tell() == 0

    def test_read_beyond_end_raises_error(self):
        """Test that reading beyond end raises IndexError."""
        data = b'\x01\x02'
        reader = BinaryReader(data)

        with pytest.raises(IndexError):
            reader.read_bytes(10)


@pytest.mark.unit
class TestBinaryWriter:
    """Test cases for BinaryWriter."""

    def test_write_bytes(self):
        """Test writing raw bytes."""
        writer = BinaryWriter()

        writer.write_bytes(b'\x01\x02\x03')
        assert writer.get_bytes() == b'\x01\x02\x03'

    def test_write_byte(self):
        """Test writing single byte."""
        writer = BinaryWriter()

        writer.write_byte(0xFF)
        writer.write_byte(0x00)
        assert writer.get_bytes() == b'\xFF\x00'

    def test_write_uint16_little_endian(self):
        """Test writing 16-bit unsigned integer."""
        writer = BinaryWriter()

        writer.write_uint16(0x0201, little_endian=True)
        assert writer.get_bytes() == b'\x01\x02'

    def test_write_string(self):
        """Test writing fixed-length string."""
        writer = BinaryWriter()

        writer.write_string("Hello", length=8)
        result = writer.get_bytes()

        assert len(result) == 8
        assert result[:5] == b'Hello'
        assert result[5:] == b'\x00\x00\x00'  # Padding

    def test_clear(self):
        """Test clearing writer."""
        writer = BinaryWriter()

        writer.write_bytes(b'\x01\x02\x03')
        assert len(writer.get_bytes()) == 3

        writer.clear()
        assert len(writer.get_bytes()) == 0


@pytest.mark.unit
class TestFileHandler:
    """Test cases for FileHandler."""

    def test_read_binary(self, sample_gp5_file):
        """Test reading binary file."""
        data = FileHandler.read_binary(sample_gp5_file)

        assert isinstance(data, bytes)
        assert len(data) > 0

    def test_write_binary(self, temp_dir):
        """Test writing binary file."""
        test_data = b'\x01\x02\x03\x04'
        file_path = temp_dir / "test.bin"

        FileHandler.write_binary(file_path, test_data, create_backup=False)

        assert file_path.exists()
        assert file_path.read_bytes() == test_data

    def test_create_backup(self, sample_gp5_file):
        """Test creating file backup."""
        backup_path = FileHandler.create_backup(sample_gp5_file)

        assert backup_path.exists()
        assert backup_path != sample_gp5_file
        assert "backup" in backup_path.name

    def test_find_preset_files(self, multiple_gp5_files):
        """Test finding preset files in directory."""
        directory = multiple_gp5_files[0].parent

        files = FileHandler.find_preset_files(directory, extensions=[".gp5"])

        assert len(files) >= 5
        assert all(f.suffix == ".gp5" for f in files)


@pytest.mark.unit
class TestHexDumper:
    """Test cases for HexDumper."""

    def test_dump_basic(self):
        """Test basic hex dump."""
        dumper = HexDumper()
        data = b'\x00\x01\x02\x03\x04\x05\x06\x07'

        result = dumper.dump(data)

        assert "00000000" in result  # Address
        assert "00 01 02 03" in result  # Hex values
        assert isinstance(result, str)

    def test_dump_with_max_bytes(self):
        """Test hex dump with byte limit."""
        dumper = HexDumper()
        data = b'\x00' * 100

        result = dumper.dump(data, max_bytes=32)

        # Should only dump first 32 bytes (2 lines)
        lines = result.strip().split('\n')
        assert len(lines) == 2

    def test_find_patterns(self):
        """Test finding byte patterns."""
        dumper = HexDumper()
        data = b'\x00\x01\xFF\xFF\x00\x01\xFF\xFF'

        offsets = dumper.find_patterns(data, b'\xFF\xFF')

        assert len(offsets) == 2
        assert 2 in offsets
        assert 6 in offsets


@pytest.mark.unit
class TestPresetValidator:
    """Test cases for PresetValidator."""

    def test_validate_parameter_range_valid(self):
        """Test validating valid parameter range."""
        is_valid, error = PresetValidator.validate_parameter_range("input_gain", 50)

        assert is_valid is True
        assert error == ""

    def test_validate_parameter_range_too_high(self):
        """Test validating parameter above range."""
        is_valid, error = PresetValidator.validate_parameter_range("input_gain", 150)

        assert is_valid is False
        assert "input_gain" in error

    def test_validate_parameter_range_invalid_type(self):
        """Test validating parameter with wrong type."""
        is_valid, error = PresetValidator.validate_parameter_range("input_gain", "invalid")

        assert is_valid is False
        assert "numeric" in error.lower()

    def test_validate_preset_name_valid(self):
        """Test validating valid preset name."""
        is_valid, error = PresetValidator.validate_preset_name("Valid Name")

        assert is_valid is True
        assert error == ""

    def test_validate_preset_name_empty(self):
        """Test validating empty preset name."""
        is_valid, error = PresetValidator.validate_preset_name("")

        assert is_valid is False
        assert "empty" in error.lower()

    def test_validate_preset_name_invalid_chars(self):
        """Test validating name with invalid characters."""
        is_valid, error = PresetValidator.validate_preset_name("Invalid/Name")

        assert is_valid is False
        assert "invalid character" in error.lower()

    def test_sanitize_preset_name(self):
        """Test sanitizing preset name."""
        dirty_name = "Test:Preset*Name?"
        clean_name = PresetValidator.sanitize_preset_name(dirty_name)

        assert ":" not in clean_name
        assert "*" not in clean_name
        assert "?" not in clean_name

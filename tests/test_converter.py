"""
Tests for the preset converter module.
"""

import pytest

from gp_presets_converter.converter import PresetConverter


class TestPresetConverter:
    """Test cases for PresetConverter class."""

    def test_converter_initialization(self):
        """Test that converter initializes correctly."""
        converter = PresetConverter()
        assert converter.version == "0.1.0"

    def test_convert_file_missing_input(self, tmp_path):
        """Test that convert_file raises FileNotFoundError for missing input."""
        converter = PresetConverter()
        input_file = tmp_path / "nonexistent.gp5"

        with pytest.raises(FileNotFoundError):
            converter.convert_file(input_file)

    def test_convert_directory_invalid_path(self, tmp_path):
        """Test that convert_directory raises NotADirectoryError for non-directory."""
        converter = PresetConverter()
        invalid_dir = tmp_path / "notadirectory.txt"
        invalid_dir.write_text("test")

        with pytest.raises(NotADirectoryError):
            converter.convert_directory(invalid_dir)

    def test_convert_directory_empty(self, tmp_path):
        """Test converting an empty directory returns empty list."""
        converter = PresetConverter()
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()

        result = converter.convert_directory(empty_dir)
        assert result == []

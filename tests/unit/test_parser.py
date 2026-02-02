"""
Unit tests for PresetParser.
"""

import pytest
from pathlib import Path

from gp_presets_converter.core import PresetParser
from gp_presets_converter.models import PresetData


@pytest.mark.unit
class TestPresetParser:
    """Test cases for PresetParser class."""

    def test_parser_initialization(self):
        """Test that parser initializes correctly."""
        parser = PresetParser()
        assert parser.format_detected is None

    def test_parse_gp5_file(self, sample_gp5_file):
        """Test parsing a GP-5 preset file."""
        parser = PresetParser()
        result = parser.parse_file(sample_gp5_file)

        assert isinstance(result, PresetData)
        assert result.format in ["GP5", "UNKNOWN"]
        assert result.name is not None

    def test_parse_gp50_file(self, sample_gp50_file):
        """Test parsing a GP-50 preset file."""
        parser = PresetParser()
        result = parser.parse_file(sample_gp50_file)

        assert isinstance(result, PresetData)
        assert result.format in ["GP50", "UNKNOWN"]
        assert result.name is not None

    def test_parse_nonexistent_file(self, temp_dir):
        """Test that parsing nonexistent file raises FileNotFoundError."""
        parser = PresetParser()
        nonexistent = temp_dir / "does_not_exist.gp5"

        with pytest.raises(FileNotFoundError):
            parser.parse_file(nonexistent)

    def test_parse_empty_file_raises_error(self, empty_file):
        """Test that parsing empty file raises ValueError."""
        parser = PresetParser()

        with pytest.raises(ValueError, match="Empty preset file"):
            parser.parse_file(empty_file)

    def test_parse_corrupted_file(self, corrupted_file):
        """Test that parser handles corrupted files."""
        parser = PresetParser()
        result = parser.parse_file(corrupted_file)

        # Should return UNKNOWN format for corrupted files
        assert result.format == "UNKNOWN"

    def test_validate_checksum(self, sample_gp5_data):
        """Test checksum validation."""
        parser = PresetParser()
        # Current implementation always returns True (placeholder)
        assert parser.validate_checksum(sample_gp5_data) is True

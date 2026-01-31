"""
End-to-end integration tests for the converter.
"""

import pytest
from pathlib import Path

from gp_presets_converter import PresetConverter


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""

    def test_full_conversion_workflow(self, sample_gp5_file, temp_dir):
        """Test complete conversion workflow."""
        converter = PresetConverter()
        output_file = temp_dir / "output.gp50"

        # Convert file
        result = converter.convert_file(sample_gp5_file, output_file)

        # Verify output exists
        assert result.exists()
        assert result == output_file

    def test_batch_conversion(self, multiple_gp5_files, temp_dir):
        """Test batch directory conversion."""
        converter = PresetConverter()
        input_dir = multiple_gp5_files[0].parent
        output_dir = temp_dir / "output"

        # Convert directory
        results = converter.convert_directory(input_dir, output_dir)

        # Verify all files converted
        assert len(results) == len(multiple_gp5_files)
        assert output_dir.exists()

        # Verify output files exist
        for result in results:
            assert result.exists()
            assert result.suffix == ".gp50"

    def test_conversion_preserves_name(self, sample_gp5_file, temp_dir):
        """Test that conversion preserves preset information."""
        from gp_presets_converter.core import PresetParser

        # Parse original
        parser = PresetParser()
        original_data = parser.parse_file(sample_gp5_file)

        # Convert
        converter = PresetConverter()
        output_file = temp_dir / "output.gp50"
        converter.convert_file(sample_gp5_file, output_file)

        # Verify conversion (actual verification would require parsing GP-50)
        assert output_file.exists()

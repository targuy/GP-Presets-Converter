"""
Unit tests for CoreConverter.
"""

import pytest

from gp_presets_converter.core import CoreConverter
from gp_presets_converter.models import GP5Preset, GP50Preset


@pytest.mark.unit
class TestCoreConverter:
    """Test cases for CoreConverter class."""

    def test_converter_initialization(self):
        """Test that converter initializes correctly."""
        converter = CoreConverter()
        assert converter.conversion_rules is not None
        assert "parameter_mapping" in converter.conversion_rules

    def test_convert_basic_preset(self):
        """Test converting a basic GP-5 preset."""
        converter = CoreConverter()

        gp5 = GP5Preset(
            name="Test Preset",
            version="1.0",
            parameters={
                "input_gain": 50,
                "output_level": 75,
                "effects_chain": []
            }
        )

        gp50 = converter.convert(gp5)

        assert isinstance(gp50, GP50Preset)
        assert gp50.name == "Test Preset"
        assert gp50.parameters["input_gain"] == 50
        assert gp50.parameters["output_level"] == 75

    def test_convert_with_effects(self):
        """Test converting preset with effects chain."""
        converter = CoreConverter()

        gp5 = GP5Preset(
            name="Test Preset",
            version="1.0",
            parameters={
                "effects_chain": [
                    {"type": "overdrive", "drive": 60, "tone": 50},
                    {"type": "delay", "time": 500, "feedback": 30}
                ]
            }
        )

        gp50 = converter.convert(gp5)

        assert len(gp50.parameters["effects_chain"]) == 2
        assert gp50.parameters["effects_chain"][0]["type"] == "overdrive"

    def test_parameter_validation(self):
        """Test parameter range validation."""
        converter = CoreConverter()

        # Test valid range
        result = converter._validate_parameter("input_gain", 50)
        assert result == 50

        # Test clamping high value
        result = converter._validate_parameter("input_gain", 150)
        assert result == 100

        # Test clamping low value
        result = converter._validate_parameter("input_gain", -10)
        assert result == 0

    def test_check_compatibility(self):
        """Test compatibility checking."""
        converter = CoreConverter()

        gp5 = GP5Preset(
            name="Test",
            version="1.0",
            parameters={
                "effects_chain": [
                    {"type": "overdrive"},  # Supported
                ]
            }
        )

        is_compatible, warnings = converter.check_compatibility(gp5)
        assert is_compatible is True
        assert len(warnings) == 0

    def test_check_compatibility_with_unknown_effect(self):
        """Test compatibility with unsupported effects."""
        converter = CoreConverter()

        gp5 = GP5Preset(
            name="Test",
            version="1.0",
            parameters={
                "effects_chain": [
                    {"type": "unknown_effect"},
                ]
            }
        )

        is_compatible, warnings = converter.check_compatibility(gp5)
        assert is_compatible is False
        assert len(warnings) > 0

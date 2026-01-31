"""
Unit tests for data models.
"""

import pytest

from gp_presets_converter.models import GP5Preset, GP50Preset, PresetData


@pytest.mark.unit
class TestPresetData:
    """Test cases for PresetData model."""

    def test_creation(self):
        """Test creating a PresetData object."""
        data = PresetData(
            format="GP5",
            version="1.0",
            name="Test",
            parameters={"input_gain": 50}
        )

        assert data.format == "GP5"
        assert data.version == "1.0"
        assert data.name == "Test"
        assert data.parameters["input_gain"] == 50

    def test_empty_name_defaults(self):
        """Test that empty name gets a default value."""
        data = PresetData(
            format="GP5",
            version="1.0",
            name="",
            parameters={}
        )

        assert data.name == "Unnamed Preset"


@pytest.mark.unit
class TestGP5Preset:
    """Test cases for GP5Preset model."""

    def test_creation_with_defaults(self):
        """Test creating GP5Preset with default values."""
        preset = GP5Preset()

        assert preset.name == "Unnamed GP-5 Preset"
        assert preset.version == "1.0"
        assert "input_gain" in preset.parameters
        assert "effects_chain" in preset.parameters

    def test_creation_with_custom_values(self):
        """Test creating GP5Preset with custom values."""
        preset = GP5Preset(
            name="Custom Preset",
            version="2.0",
            parameters={"input_gain": 75}
        )

        assert preset.name == "Custom Preset"
        assert preset.version == "2.0"
        assert preset.parameters["input_gain"] == 75

    def test_to_dict(self):
        """Test converting preset to dictionary."""
        preset = GP5Preset(name="Test", version="1.0", parameters={})
        result = preset.to_dict()

        assert result["format"] == "GP5"
        assert result["name"] == "Test"
        assert result["version"] == "1.0"
        assert isinstance(result["parameters"], dict)

    def test_from_dict(self):
        """Test loading preset from dictionary."""
        data = {
            "format": "GP5",
            "name": "Test",
            "version": "1.0",
            "parameters": {"input_gain": 50}
        }

        preset = GP5Preset()
        preset.from_dict(data)

        assert preset.name == "Test"
        assert preset.version == "1.0"
        assert preset.parameters["input_gain"] == 50

    def test_from_dict_invalid_format(self):
        """Test that from_dict raises error for invalid format."""
        data = {
            "format": "GP50",  # Wrong format
            "name": "Test",
            "version": "1.0",
            "parameters": {}
        }

        preset = GP5Preset()
        with pytest.raises(ValueError, match="Invalid format"):
            preset.from_dict(data)

    def test_validate_success(self):
        """Test validation of valid preset."""
        preset = GP5Preset(
            name="Valid Preset",
            version="1.0",
            parameters={
                "input_gain": 50,
                "output_level": 75,
                "effects_chain": []
            }
        )

        is_valid, errors = preset.validate()
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_empty_name(self):
        """Test validation fails for empty name."""
        preset = GP5Preset(name="", version="1.0", parameters={})

        is_valid, errors = preset.validate()
        assert is_valid is False
        assert any("name" in error.lower() for error in errors)

    def test_validate_invalid_input_gain(self):
        """Test validation fails for invalid parameter range."""
        preset = GP5Preset(
            name="Test",
            version="1.0",
            parameters={"input_gain": 150}  # Out of range
        )

        is_valid, errors = preset.validate()
        assert is_valid is False
        assert any("input" in error.lower() and "gain" in error.lower() for error in errors)

    def test_add_effect(self):
        """Test adding effect to chain."""
        preset = GP5Preset()

        effect = {"type": "overdrive", "drive": 60}
        preset.add_effect(effect)

        assert len(preset.get_effect_chain()) == 1
        assert preset.get_effect_chain()[0]["type"] == "overdrive"

    def test_remove_effect(self):
        """Test removing effect from chain."""
        preset = GP5Preset()

        preset.add_effect({"type": "overdrive"})
        preset.add_effect({"type": "delay"})

        assert len(preset.get_effect_chain()) == 2

        preset.remove_effect(0)
        assert len(preset.get_effect_chain()) == 1
        assert preset.get_effect_chain()[0]["type"] == "delay"

    def test_remove_effect_invalid_index(self):
        """Test that removing with invalid index raises error."""
        preset = GP5Preset()

        with pytest.raises(IndexError):
            preset.remove_effect(999)


@pytest.mark.unit
class TestGP50Preset:
    """Test cases for GP50Preset model."""

    def test_creation_with_defaults(self):
        """Test creating GP50Preset with default values."""
        preset = GP50Preset()

        assert preset.name == "Unnamed GP-50 Preset"
        assert preset.version == "1.0"
        assert "expression_pedal_assignment" in preset.parameters

    def test_set_expression_pedal(self):
        """Test setting expression pedal assignment."""
        preset = GP50Preset()

        preset.set_expression_pedal("wah_position")
        assert preset.parameters["expression_pedal_assignment"] == "wah_position"

    def test_validate_success(self):
        """Test validation of valid preset."""
        preset = GP50Preset(
            name="Valid Preset",
            version="1.0",
            parameters={
                "input_gain": 50,
                "output_level": 75,
                "effects_chain": []
            }
        )

        is_valid, errors = preset.validate()
        assert is_valid is True
        assert len(errors) == 0

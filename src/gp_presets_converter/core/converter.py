"""
GP-5 to GP-50 conversion logic.

This module handles the core conversion logic between GP-5 and GP-50 formats,
including parameter mapping and validation.
"""

from typing import Dict, Any

from ..models.common import PresetData
from ..models.gp5_preset import GP5Preset
from ..models.gp50_preset import GP50Preset


class CoreConverter:
    """
    Core converter for translating GP-5 presets to GP-50 format.

    This class handles the parameter mapping and translation between
    the two formats, accounting for differences in capabilities and
    parameter ranges.
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
        # Placeholder conversion rules
        # These would be determined through analysis of actual presets
        return {
            "parameter_mapping": {
                "input_gain": "input_gain",
                "output_level": "output_level",
            },
            "effect_mapping": {
                # Effects that exist in both formats
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
        Convert a GP-5 preset to GP-50 format.

        Args:
            gp5_preset: GP5Preset object to convert

        Returns:
            GP50Preset object with converted parameters

        Raises:
            ValueError: If conversion is not possible
        """
        # Create new GP-50 preset with mapped parameters
        converted_params: Dict[str, Any] = {}

        # Map basic parameters
        for gp5_key, gp50_key in self.conversion_rules["parameter_mapping"].items():
            if gp5_key in gp5_preset.parameters:
                value = gp5_preset.parameters[gp5_key]
                converted_params[gp50_key] = self._validate_parameter(gp50_key, value)

        # Map effects chain
        converted_effects = []
        for effect in gp5_preset.parameters.get("effects_chain", []):
            if isinstance(effect, dict):
                effect_type = effect.get("type", "")
                if effect_type in self.conversion_rules["effect_mapping"]:
                    converted_effects.append(effect)

        converted_params["effects_chain"] = converted_effects

        # Create GP-50 preset
        gp50_preset = GP50Preset(
            name=gp5_preset.name,
            version="1.0",
            parameters=converted_params,
        )

        return gp50_preset

    def _validate_parameter(self, param_name: str, value: Any) -> Any:
        """
        Validate and clamp parameter value to valid range.

        Args:
            param_name: Name of the parameter
            value: Parameter value to validate

        Returns:
            Validated parameter value
        """
        if param_name in self.conversion_rules["parameter_ranges"]:
            min_val, max_val = self.conversion_rules["parameter_ranges"][param_name]
            if isinstance(value, (int, float)):
                return max(min_val, min(max_val, value))

        return value

    def check_compatibility(self, gp5_preset: GP5Preset) -> tuple[bool, list[str]]:
        """
        Check if a GP-5 preset can be fully converted to GP-50.

        Args:
            gp5_preset: GP5Preset object to check

        Returns:
            Tuple of (is_compatible, list_of_warnings)
        """
        warnings = []
        is_compatible = True

        # Check for unsupported effects
        for effect in gp5_preset.parameters.get("effects_chain", []):
            if isinstance(effect, dict):
                effect_type = effect.get("type", "")
                if effect_type not in self.conversion_rules["effect_mapping"]:
                    warnings.append(f"Effect '{effect_type}' may not be supported in GP-50")
                    is_compatible = False

        return is_compatible, warnings

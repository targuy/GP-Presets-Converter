"""
Data validation utilities for presets.

This module provides validation functions for preset data structures.
"""

from typing import Any, Dict, List, Tuple

from ..models.preset import BasePreset


class PresetValidator:
    """
    Validator for preset data structures.

    Provides comprehensive validation of preset parameters and structure.
    """

    # Valid parameter ranges
    PARAMETER_RANGES = {
        "input_gain": (0, 100),
        "output_level": (0, 100),
        "noise_gate_threshold": (0, 100),
        "mix": (0, 100),
        "level": (0, 100),
        "drive": (0, 100),
        "tone": (0, 100),
        "gain": (0, 100),
        "feedback": (0, 100),
        "rate": (0, 100),
        "depth": (0, 100),
        "bass": (0, 100),
        "mid": (0, 100),
        "treble": (0, 100),
        "presence": (0, 100),
        "master": (0, 100),
    }

    # Valid effect types
    VALID_EFFECT_TYPES = {
        "overdrive",
        "distortion",
        "fuzz",
        "boost",
        "delay",
        "reverb",
        "chorus",
        "flanger",
        "phaser",
        "tremolo",
        "compressor",
        "eq",
        "wah",
        "amp_sim",
        "cabinet",
        "noise_gate",
    }

    @staticmethod
    def validate_preset(preset: BasePreset) -> Tuple[bool, List[str]]:
        """
        Validate a preset object.

        Args:
            preset: Preset object to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        return preset.validate()

    @staticmethod
    def validate_parameter_range(name: str, value: Any) -> Tuple[bool, str]:
        """
        Validate that a parameter value is within its valid range.

        Args:
            name: Parameter name
            value: Parameter value

        Returns:
            Tuple of (is_valid, error_message)
        """
        if name not in PresetValidator.PARAMETER_RANGES:
            return True, ""  # Unknown parameter, no validation

        min_val, max_val = PresetValidator.PARAMETER_RANGES[name]

        if not isinstance(value, (int, float)):
            return False, f"Parameter '{name}' must be numeric, got {type(value).__name__}"

        if value < min_val or value > max_val:
            return (
                False,
                f"Parameter '{name}' must be between {min_val} and {max_val}, got {value}",
            )

        return True, ""

    @staticmethod
    def validate_effect(effect: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate an effect dictionary.

        Args:
            effect: Effect dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check for required fields
        if "type" not in effect:
            errors.append("Effect missing required 'type' field")
            return False, errors

        effect_type = effect["type"]

        # Validate effect type
        if effect_type not in PresetValidator.VALID_EFFECT_TYPES:
            errors.append(f"Unknown effect type: {effect_type}")

        # Validate common parameters
        for param in ["enabled", "bypass"]:
            if param in effect and not isinstance(effect[param], bool):
                errors.append(f"Effect parameter '{param}' must be boolean")

        # Validate numeric parameters
        for param, value in effect.items():
            if param in ["type", "enabled", "bypass"]:
                continue

            if isinstance(value, (int, float)):
                is_valid, error = PresetValidator.validate_parameter_range(param, value)
                if not is_valid:
                    errors.append(error)

        return len(errors) == 0, errors

    @staticmethod
    def validate_effects_chain(effects: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Validate an entire effects chain.

        Args:
            effects: List of effect dictionaries

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not isinstance(effects, list):
            return False, ["Effects chain must be a list"]

        for i, effect in enumerate(effects):
            if not isinstance(effect, dict):
                errors.append(f"Effect {i} must be a dictionary")
                continue

            is_valid, effect_errors = PresetValidator.validate_effect(effect)
            if not is_valid:
                for error in effect_errors:
                    errors.append(f"Effect {i}: {error}")

        return len(errors) == 0, errors

    @staticmethod
    def validate_preset_name(name: str) -> Tuple[bool, str]:
        """
        Validate a preset name.

        Args:
            name: Preset name to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(name, str):
            return False, "Preset name must be a string"

        if len(name.strip()) == 0:
            return False, "Preset name cannot be empty"

        if len(name) > 64:
            return False, "Preset name too long (maximum 64 characters)"

        # Check for invalid characters (varies by format)
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in name:
                return False, f"Preset name contains invalid character: {char}"

        return True, ""

    @staticmethod
    def sanitize_preset_name(name: str) -> str:
        """
        Sanitize a preset name by removing invalid characters.

        Args:
            name: Preset name to sanitize

        Returns:
            Sanitized preset name
        """
        # Remove invalid characters
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        sanitized = name
        for char in invalid_chars:
            sanitized = sanitized.replace(char, '_')

        # Trim to max length
        sanitized = sanitized[:64]

        # Ensure not empty
        if not sanitized.strip():
            sanitized = "Unnamed Preset"

        return sanitized

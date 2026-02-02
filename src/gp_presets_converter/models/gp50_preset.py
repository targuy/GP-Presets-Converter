"""
GP-50 specific preset model.

This module defines the data structure for VALETON GP-50 presets.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .preset import BasePreset


@dataclass
class GP50Preset(BasePreset):
    """
    Data model for VALETON GP-50 presets.

    The GP-50 shares the same internal engine as the GP-5 but has
    different I/O configurations and user interface.
    """

    name: str = "Unnamed GP-50 Preset"
    version: str = "1.0"
    parameters: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Initialize default parameters if not provided."""
        if not self.parameters:
            self.parameters = {
                "input_gain": 50,
                "output_level": 50,
                "effects_chain": [],
                "noise_gate_enabled": False,
                "noise_gate_threshold": 30,
                "expression_pedal_assignment": None,
            }

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert preset to dictionary representation.

        Returns:
            Dictionary containing all preset data
        """
        return {
            "format": "GP50",
            "name": self.name,
            "version": self.version,
            "parameters": self.parameters.copy(),
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load preset from dictionary representation.

        Args:
            data: Dictionary containing preset data

        Raises:
            ValueError: If data format is invalid
        """
        if data.get("format") != "GP50":
            raise ValueError(f"Invalid format: expected GP50, got {data.get('format')}")

        self.name = data.get("name", "Unnamed GP-50 Preset")
        self.version = data.get("version", "1.0")
        self.parameters = data.get("parameters", {})

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate the preset data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Validate name
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Preset name cannot be empty")

        # Validate input gain
        input_gain = self.parameters.get("input_gain")
        if input_gain is not None and not (0 <= input_gain <= 100):
            errors.append(f"Input gain must be 0-100, got {input_gain}")

        # Validate output level
        output_level = self.parameters.get("output_level")
        if output_level is not None and not (0 <= output_level <= 100):
            errors.append(f"Output level must be 0-100, got {output_level}")

        # Validate effects chain
        effects_chain = self.parameters.get("effects_chain", [])
        if not isinstance(effects_chain, list):
            errors.append("Effects chain must be a list")

        return len(errors) == 0, errors

    def get_effect_count(self) -> int:
        """
        Get the number of effects in the chain.

        Returns:
            Number of effects
        """
        return len(self.parameters.get("effects_chain", []))

    def add_effect(self, effect: Dict[str, Any]) -> None:
        """
        Add an effect to the chain.

        Args:
            effect: Effect dictionary with type and parameters
        """
        if "effects_chain" not in self.parameters:
            self.parameters["effects_chain"] = []

        self.parameters["effects_chain"].append(effect)

    def remove_effect(self, index: int) -> None:
        """
        Remove an effect from the chain by index.

        Args:
            index: Index of effect to remove

        Raises:
            IndexError: If index is out of range
        """
        effects = self.parameters.get("effects_chain", [])
        if 0 <= index < len(effects):
            effects.pop(index)
        else:
            raise IndexError(f"Effect index {index} out of range")

    def set_expression_pedal(self, parameter: str) -> None:
        """
        Assign expression pedal to control a parameter.

        Args:
            parameter: Parameter name to control with expression pedal
        """
        self.parameters["expression_pedal_assignment"] = parameter

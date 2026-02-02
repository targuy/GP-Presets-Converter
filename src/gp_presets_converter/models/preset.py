"""
Base preset data structures.

This module defines the abstract base class for all preset types.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class BasePreset(ABC):
    """
    Abstract base class for all preset types.

    This class defines the common interface that all preset formats must implement.
    """

    name: str
    version: str
    parameters: Dict[str, Any] = field(default_factory=dict)

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert preset to dictionary representation.

        Returns:
            Dictionary containing all preset data
        """
        pass

    @abstractmethod
    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Load preset from dictionary representation.

        Args:
            data: Dictionary containing preset data
        """
        pass

    @abstractmethod
    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate the preset data.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        pass

    def get_effect_chain(self) -> List[Dict[str, Any]]:
        """
        Get the effects chain from parameters.

        Returns:
            List of effect dictionaries
        """
        return self.parameters.get("effects_chain", [])

    def set_effect_chain(self, effects: List[Dict[str, Any]]) -> None:
        """
        Set the effects chain in parameters.

        Args:
            effects: List of effect dictionaries
        """
        self.parameters["effects_chain"] = effects

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """
        Get a parameter value by key.

        Args:
            key: Parameter key
            default: Default value if key doesn't exist

        Returns:
            Parameter value or default
        """
        return self.parameters.get(key, default)

    def set_parameter(self, key: str, value: Any) -> None:
        """
        Set a parameter value.

        Args:
            key: Parameter key
            value: Parameter value
        """
        self.parameters[key] = value

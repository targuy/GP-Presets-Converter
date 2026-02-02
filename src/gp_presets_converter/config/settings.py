"""
Configuration settings for GP Presets Converter.

This module contains configuration options and constants used throughout
the application.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Settings:
    """
    Configuration settings for the converter.

    These settings control various aspects of the conversion process
    and application behavior.
    """

    # Supported file extensions
    GP5_EXTENSIONS: List[str] = None
    GP50_EXTENSIONS: List[str] = None
    ALL_PRESET_EXTENSIONS: List[str] = None

    # File size limits (in bytes)
    MIN_PRESET_SIZE: int = 64
    MAX_PRESET_SIZE: int = 10 * 1024 * 1024  # 10 MB

    # Conversion options
    CREATE_BACKUP: bool = True
    OVERWRITE_EXISTING: bool = False
    VALIDATE_OUTPUT: bool = True

    # Logging options
    VERBOSE: bool = False
    DEBUG: bool = False

    # Analysis options
    HEX_DUMP_BYTES_PER_LINE: int = 16
    HEX_DUMP_MAX_BYTES: int = 1024

    # Performance options
    ENABLE_PROGRESS_BAR: bool = True
    BATCH_SIZE: int = 10

    def __post_init__(self) -> None:
        """Initialize default values."""
        if self.GP5_EXTENSIONS is None:
            self.GP5_EXTENSIONS = [".gp5", ".GP5"]

        if self.GP50_EXTENSIONS is None:
            self.GP50_EXTENSIONS = [".gp50", ".GP50"]

        if self.ALL_PRESET_EXTENSIONS is None:
            self.ALL_PRESET_EXTENSIONS = self.GP5_EXTENSIONS + self.GP50_EXTENSIONS + [".preset"]

    @classmethod
    def default(cls) -> "Settings":
        """
        Create settings with default values.

        Returns:
            Settings object with default configuration
        """
        return cls()

    @classmethod
    def for_analysis(cls) -> "Settings":
        """
        Create settings optimized for binary analysis.

        Returns:
            Settings object configured for analysis mode
        """
        settings = cls()
        settings.VERBOSE = True
        settings.DEBUG = True
        settings.HEX_DUMP_MAX_BYTES = 4096
        return settings

    @classmethod
    def for_batch_conversion(cls) -> "Settings":
        """
        Create settings optimized for batch conversion.

        Returns:
            Settings object configured for batch processing
        """
        settings = cls()
        settings.CREATE_BACKUP = True
        settings.ENABLE_PROGRESS_BAR = True
        settings.BATCH_SIZE = 50
        return settings

    def to_dict(self) -> dict:
        """
        Convert settings to dictionary.

        Returns:
            Dictionary representation of settings
        """
        return {
            "gp5_extensions": self.GP5_EXTENSIONS,
            "gp50_extensions": self.GP50_EXTENSIONS,
            "all_preset_extensions": self.ALL_PRESET_EXTENSIONS,
            "min_preset_size": self.MIN_PRESET_SIZE,
            "max_preset_size": self.MAX_PRESET_SIZE,
            "create_backup": self.CREATE_BACKUP,
            "overwrite_existing": self.OVERWRITE_EXISTING,
            "validate_output": self.VALIDATE_OUTPUT,
            "verbose": self.VERBOSE,
            "debug": self.DEBUG,
            "hex_dump_bytes_per_line": self.HEX_DUMP_BYTES_PER_LINE,
            "hex_dump_max_bytes": self.HEX_DUMP_MAX_BYTES,
            "enable_progress_bar": self.ENABLE_PROGRESS_BAR,
            "batch_size": self.BATCH_SIZE,
        }


# Global default settings instance
DEFAULT_SETTINGS = Settings.default()

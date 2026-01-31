"""
GP Presets Converter - Convert VALETON GP-5 presets to GP-50 format.

This package provides tools to convert preset files between VALETON
multi-effects pedal formats (GP-5 to GP-50).
"""

__version__ = "0.1.0"
__author__ = "GP Presets Converter Contributors"

from .converter import PresetConverter

__all__ = ["PresetConverter"]

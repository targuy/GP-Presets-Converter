"""
GP Presets Converter - Convert VALETON GP-5 presets to GP-50 format.

This package provides tools to convert preset files between VALETON
multi-effects pedal formats (GP-5 to GP-50).
"""

__version__ = "0.1.0"
__author__ = "GP Presets Converter Contributors"

from .converter import PresetConverter
from .core import BinaryAnalyzer, CoreConverter, PresetParser, PresetWriter
from .models import GP5Preset, GP50Preset, PresetData

__all__ = [
    "PresetConverter",
    "BinaryAnalyzer",
    "CoreConverter",
    "PresetParser",
    "PresetWriter",
    "GP5Preset",
    "GP50Preset",
    "PresetData",
]

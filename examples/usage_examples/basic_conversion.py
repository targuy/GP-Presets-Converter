#!/usr/bin/env python3
"""
Basic Conversion Example

This script demonstrates basic single-file conversion from GP-5 to GP-50 format.
"""

from pathlib import Path
from gp_presets_converter import PresetConverter


def main():
    """Perform a basic preset file conversion."""
    # Initialize the converter
    converter = PresetConverter()

    # Define input and output paths
    input_file = Path("../valeton_presets/gp5/factory/example_preset.gp5")
    output_file = Path("../valeton_presets/gp50/factory/example_preset.gp50")

    # Check if input file exists
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        print("Please add a GP-5 preset file to convert.")
        return 1

    # Perform the conversion
    try:
        print(f"Converting: {input_file}")
        result = converter.convert_file(input_file, output_file)
        print(f"✓ Successfully converted to: {result}")
        return 0

    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

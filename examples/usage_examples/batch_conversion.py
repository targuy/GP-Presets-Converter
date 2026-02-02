#!/usr/bin/env python3
"""
Batch Conversion Example

This script demonstrates batch conversion of all GP-5 presets in a directory
to GP-50 format, with progress tracking and error handling.
"""

import sys
from pathlib import Path
from gp_presets_converter import PresetConverter
from gp_presets_converter.utils import FileHandler


def main():
    """Perform batch conversion of preset files."""
    # Define input and output directories
    input_dir = Path("../valeton_presets/gp5/user")
    output_dir = Path("../valeton_presets/gp50/user")

    # Check if input directory exists
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return 1

    # Create output directory if it doesn't exist
    FileHandler.ensure_directory(output_dir)

    # Find all GP-5 preset files
    preset_files = FileHandler.find_preset_files(input_dir, extensions=[".gp5"])

    if not preset_files:
        print(f"No GP-5 preset files found in {input_dir}")
        return 0

    print(f"Found {len(preset_files)} preset file(s) to convert")
    print(f"Output directory: {output_dir}")
    print()

    # Initialize converter
    converter = PresetConverter()

    # Track conversion results
    successful = []
    failed = []

    # Convert each file
    for i, input_file in enumerate(preset_files, 1):
        # Generate output filename
        output_file = output_dir / input_file.with_suffix(".gp50").name

        try:
            print(f"[{i}/{len(preset_files)}] Converting {input_file.name}...", end=" ")
            sys.stdout.flush()

            result = converter.convert_file(input_file, output_file)
            successful.append(result)
            print("✓")

        except Exception as e:
            failed.append((input_file, str(e)))
            print(f"✗ Error: {e}")

    # Print summary
    print()
    print("=" * 60)
    print("Conversion Summary")
    print("=" * 60)
    print(f"Total files:      {len(preset_files)}")
    print(f"Successful:       {len(successful)}")
    print(f"Failed:           {len(failed)}")

    if failed:
        print()
        print("Failed conversions:")
        for file_path, error in failed:
            print(f"  - {file_path.name}: {error}")

    return 0 if not failed else 1


if __name__ == "__main__":
    exit(main())

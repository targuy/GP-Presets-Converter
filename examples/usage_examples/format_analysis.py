#!/usr/bin/env python3
"""
Format Analysis Example

This script demonstrates how to analyze binary preset files to understand
their structure and content.
"""

import sys
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer
from gp_presets_converter.utils import FileHandler, HexDumper


def analyze_single_file(file_path: Path):
    """Analyze a single preset file."""
    print(f"\n{'=' * 70}")
    print(f"Analyzing: {file_path}")
    print('=' * 70)

    # Initialize analyzer
    analyzer = BinaryAnalyzer()

    try:
        # Perform analysis
        analysis = analyzer.analyze_file(file_path)

        # Display results
        print(f"\nFile Information:")
        print(f"  Size: {analysis['file_size']} bytes")
        print(f"  Signature (first 16 bytes): {analysis['signature']}")

        print(f"\nByte Distribution:")
        dist = analysis['byte_distribution']
        print(f"  Min value: {dist['min']}")
        print(f"  Max value: {dist['max']}")
        print(f"  Mean value: {dist['mean']:.2f}")
        print(f"  Null bytes: {dist['null_bytes']} ({dist['null_percentage']:.1f}%)")

        print(f"\nDetected Strings:")
        if analysis['possible_strings']:
            for s in analysis['possible_strings'][:10]:
                print(f"  - '{s}'")
        else:
            print("  None found")

        print(f"\nRepeating Patterns:")
        if analysis['repeating_patterns']:
            for pattern, count in analysis['repeating_patterns'][:5]:
                hex_pattern = ' '.join(f'{b:02X}' for b in pattern)
                print(f"  - {hex_pattern} (occurs {count} times)")
        else:
            print("  None found")

        print(f"\nStructure Hints:")
        hints = analysis['structure_hints']
        print(f"  Guessed header size: {hints['header_size_guess']} bytes")
        if hints['section_boundaries']:
            print(f"  Detected {len(hints['section_boundaries'])} potential section boundaries")

        print(f"\nHex Preview (first 256 bytes):")
        print(analysis['hex_preview'])

        return 0

    except Exception as e:
        print(f"Error analyzing file: {e}")
        return 1


def compare_two_files(file1: Path, file2: Path):
    """Compare two preset files to identify differences."""
    print(f"\n{'=' * 70}")
    print(f"Comparing Files")
    print('=' * 70)
    print(f"File 1: {file1}")
    print(f"File 2: {file2}")

    # Initialize analyzer
    analyzer = BinaryAnalyzer()

    try:
        # Perform comparison
        comparison = analyzer.compare_files(file1, file2)

        # Display results
        print(f"\nComparison Results:")
        print(f"  File 1 size: {comparison['file1_size']} bytes")
        print(f"  File 2 size: {comparison['file2_size']} bytes")
        print(f"  Size difference: {comparison['size_difference']} bytes")
        print(f"  Byte differences: {comparison['byte_differences']}")
        print(f"  Similarity: {comparison['similarity_percentage']:.1f}%")

        if comparison['first_differences']:
            print(f"\nFirst 20 Byte Differences:")
            for diff in comparison['first_differences'][:20]:
                offset = diff['offset']
                val1 = diff['file1_value']
                val2 = diff['file2_value']
                print(f"  Offset {offset:06X}: {val1} -> {val2}")

        return 0

    except Exception as e:
        print(f"Error comparing files: {e}")
        return 1


def main():
    """Main function for format analysis."""
    # Example 1: Analyze a single file
    test_file = Path("../test_files/simple_gp5.preset")

    if test_file.exists():
        analyze_single_file(test_file)
    else:
        print(f"Test file not found: {test_file}")
        print("Please add a preset file to analyze.")

    # Example 2: Compare two files (if they exist)
    file1 = Path("../valeton_presets/gp5/factory/preset1.gp5")
    file2 = Path("../valeton_presets/gp5/factory/preset2.gp5")

    if file1.exists() and file2.exists():
        compare_two_files(file1, file2)

    # Example 3: Generate hex dump to file
    if test_file.exists():
        print(f"\n{'=' * 70}")
        print("Generating Hex Dump File")
        print('=' * 70)

        data = FileHandler.read_binary(test_file)
        dumper = HexDumper()
        hex_output = dumper.dump(data, max_bytes=1024)

        output_file = Path("../valeton_presets/analysis/hex_dumps/example_dump.txt")
        FileHandler.ensure_directory(output_file.parent)

        with open(output_file, "w") as f:
            f.write(f"Hex dump of: {test_file}\n")
            f.write(f"File size: {len(data)} bytes\n")
            f.write("=" * 70 + "\n\n")
            f.write(hex_output)

        print(f"Hex dump saved to: {output_file}")

    return 0


if __name__ == "__main__":
    exit(main())

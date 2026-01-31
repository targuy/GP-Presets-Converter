"""
Command-line interface for GP Presets Converter.
"""

import argparse
import sys
from pathlib import Path

from . import __version__
from .converter import PresetConverter


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert VALETON GP-5 preset files to GP-50 format",
        prog="gp-convert",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input GP-5 preset file or directory",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file or directory (optional)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    try:
        converter = PresetConverter()

        if args.input.is_file():
            output_path = converter.convert_file(args.input, args.output)
            print(f"✓ Converted: {output_path}")
        elif args.input.is_dir():
            converted_files = converter.convert_directory(args.input, args.output)
            print(f"✓ Converted {len(converted_files)} file(s)")
            if args.verbose:
                for file_path in converted_files:
                    print(f"  - {file_path}")
        else:
            print(f"Error: {args.input} is not a valid file or directory", file=sys.stderr)
            return 1

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

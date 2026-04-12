"""
Command-line interface for GP Presets Converter.

Supports bidirectional conversion between VALETON GP-5 and GP-50 .prst formats.
"""

import argparse
import sys
from pathlib import Path

from . import __version__
from .converter import PresetConverter
from .core import BinaryAnalyzer


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Convert VALETON GP-5 / GP-50 preset files (.prst) in both directions",
        prog="gp-convert",
        epilog=(
            "Examples:\n"
            "  gp-convert 55-TimPierce.prst                    # Auto-detect & convert\n"
            "  gp-convert 55-TimPierce.prst --slot 70           # Output as 70-TimPierce.prst\n"
            "  gp-convert ./GP5\\ PRESETS/ -o ./GP50/ --slot 60  # Batch starting at slot 60\n"
            "  gp-convert preset.prst --nam-offset 5            # Shift NAM refs by +5\n"
            "  gp-convert preset.prst --analyze                 # Analyze file structure\n"
            "\n"
            "For more information, see: https://github.com/targuy/GP-Presets-Converter"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Input preset file (.prst) or directory",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file or directory (optional)",
    )

    parser.add_argument(
        "-t",
        "--target",
        choices=["GP5", "GP50"],
        help="Target format (auto-detected if not specified)",
    )

    parser.add_argument(
        "-s",
        "--slot",
        type=int,
        default=None,
        metavar="N",
        help=(
            "Target slot number (0-127). Sets the leading number in the output "
            "filename. For directories, files are numbered sequentially starting "
            "from this value."
        ),
    )

    parser.add_argument(
        "--nam-offset",
        type=int,
        default=0,
        metavar="N",
        help=(
            "Signed offset to apply to NAM/SnapTone slot references inside the "
            "binary preset data. Use when NAM models are loaded in different "
            "slots on the source vs target device. "
            "Example: if NAM 'JazzClean' is in slot 51 on GP5 but slot 56 on "
            "GP50, use --nam-offset 5 when converting GP5->GP50. (default: 0)"
        ),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    parser.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze file format instead of converting",
    )

    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files before converting",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of files to process at once (default: 10)",
    )

    args = parser.parse_args()

    try:
        # Analysis mode
        if args.analyze:
            return analyze_files(args.input, args.verbose)

        # Conversion mode
        converter = PresetConverter()

        if args.input.is_file():
            output_path = converter.convert_file(
                args.input,
                args.output,
                args.target,
                target_slot=args.slot,
                nam_offset=args.nam_offset,
            )
            print(f"✓ Converted: {output_path}")
        elif args.input.is_dir():
            converted_files = converter.convert_directory(
                args.input,
                args.output,
                args.target,
                start_slot=args.slot,
                nam_offset=args.nam_offset,
            )
            print(f"✓ Converted {len(converted_files)} file(s)")
            if args.verbose:
                for file_path in converted_files:
                    print(f"  - {file_path}")
        else:
            print(f"Error: {args.input} is not a valid file or directory", file=sys.stderr)
            return 1

        return 0

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


def analyze_files(input_path: Path, verbose: bool) -> int:
    """
    Analyze preset files and display format information.

    Args:
        input_path: Path to file or directory to analyze
        verbose: Whether to show verbose output

    Returns:
        Exit code (0 for success)
    """
    analyzer = BinaryAnalyzer()

    if input_path.is_file():
        return analyze_single_file(analyzer, input_path, verbose)
    elif input_path.is_dir():
        return analyze_directory(analyzer, input_path, verbose)
    else:
        print(f"Error: {input_path} is not a valid file or directory", file=sys.stderr)
        return 1


def analyze_single_file(analyzer: BinaryAnalyzer, file_path: Path, verbose: bool) -> int:
    """Analyze a single file and display results."""
    print(f"\nAnalyzing: {file_path}")
    print("=" * 70)

    try:
        analysis = analyzer.analyze_file(file_path)

        print(f"\nFile Information:")
        print(f"  Size: {analysis['file_size']} bytes")
        print(f"  Signature: {analysis['signature']}")

        if verbose:
            print(f"\nByte Distribution:")
            dist = analysis["byte_distribution"]
            print(f"  Min value: {dist['min']}")
            print(f"  Max value: {dist['max']}")
            print(f"  Mean value: {dist['mean']:.2f}")
            print(f"  Null bytes: {dist['null_bytes']} ({dist['null_percentage']:.1f}%)")

        print(f"\nDetected Strings:")
        if analysis["possible_strings"]:
            for s in analysis["possible_strings"][:10]:
                print(f"  - '{s}'")
        else:
            print("  None found")

        if verbose:
            print(f"\nHex Preview (first 256 bytes):")
            print(analysis["hex_preview"])

        return 0

    except Exception as e:
        print(f"Error analyzing file: {e}", file=sys.stderr)
        return 1


def analyze_directory(analyzer: BinaryAnalyzer, dir_path: Path, verbose: bool) -> int:
    """Analyze all preset files in a directory."""
    from .utils import FileHandler

    print(f"\nAnalyzing directory: {dir_path}")
    print("=" * 70)

    preset_files = FileHandler.find_preset_files(dir_path)

    if not preset_files:
        print("No preset files found")
        return 0

    print(f"\nFound {len(preset_files)} preset file(s)\n")

    for i, file_path in enumerate(preset_files, 1):
        print(f"[{i}/{len(preset_files)}] {file_path.name}")

        try:
            analysis = analyzer.analyze_file(file_path)
            print(f"  Size: {analysis['file_size']} bytes")
            print(f"  Signature: {analysis['signature']}")

            if verbose and analysis["possible_strings"]:
                print(f"  Strings: {', '.join(analysis['possible_strings'][:3])}")

        except Exception as e:
            print(f"  Error: {e}")

        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

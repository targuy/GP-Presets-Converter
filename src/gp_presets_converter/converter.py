"""
Preset converter module for VALETON GP-5 / GP-50 bidirectional conversion.

This module handles the conversion logic between GP-5 and GP-50 .prst preset formats.
While the internal engine and modules are shared, the binary file structure differs.
"""

from pathlib import Path
from typing import Optional

from .core.converter import CoreConverter
from .core.parser import PresetParser
from .core.writer import PresetWriter
from .models.gp5_preset import GP5Preset
from .models.gp50_preset import GP50Preset


class PresetConverter:
    """
    Convert VALETON preset files between GP-5 and GP-50 formats.

    Supports both .prst binary files (real hardware format) and
    legacy model-based conversion. For .prst files, the converter
    operates directly on the binary data performing structural
    transformations without loss of effect parameter data.
    """

    def __init__(self) -> None:
        """Initialize the preset converter."""
        self.version = "0.1.0"
        self._parser = PresetParser()
        self._core_converter = CoreConverter()
        self._writer = PresetWriter()

    def convert_file(
        self,
        input_path: Path,
        output_path: Optional[Path] = None,
        target_format: Optional[str] = None,
    ) -> Path:
        """
        Convert a preset file between GP-5 and GP-50 formats.

        For .prst files, automatically detects the source format and
        converts to the opposite format. The target_format parameter
        can override this behavior.

        Args:
            input_path: Path to the input preset file
            output_path: Optional path for the output file
            target_format: Optional target format ("GP5" or "GP50").
                          If not provided, converts to the opposite format.

        Returns:
            Path to the converted preset file

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input file is not a valid preset
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        # Read input file
        with open(input_path, "rb") as f:
            data = f.read()

        # Detect format
        detected_format = CoreConverter.detect_format(data)

        # Determine target
        if target_format is None:
            target_format = "GP50" if detected_format == "GP5" else "GP5"

        # Determine output path
        if output_path is None:
            # Check if this is a real .prst file
            is_real_prst = (
                (data[:5] == b"GP-5\x00" and len(data) == 507)
                or (data[:5] == b"GP-50" and len(data) == 552)
            )
            if is_real_prst:
                output_path = input_path.with_suffix(".prst")
                if output_path == input_path:
                    stem = input_path.stem
                    output_path = input_path.parent / f"{stem}_{target_format.lower()}.prst"
            else:
                # Legacy format: use appropriate extension
                ext = ".gp50" if target_format == "GP50" else ".gp5"
                output_path = input_path.with_suffix(ext)

        print(f"Converting {input_path.name} ({detected_format} -> {target_format})")

        # Check if this is a real .prst file (correct size and magic)
        is_real_gp5 = data[:5] == b"GP-5\x00" and len(data) == 507
        is_real_gp50 = data[:5] == b"GP-50" and len(data) == 552

        if is_real_gp5 and target_format == "GP50":
            converted_data = CoreConverter.convert_gp5_to_gp50(data)
        elif is_real_gp50 and target_format == "GP5":
            converted_data = CoreConverter.convert_gp50_to_gp5(data)
        elif is_real_gp5 or is_real_gp50:
            raise ValueError(
                f"Cannot convert {detected_format} to {target_format}"
            )
        else:
            # Legacy/test format: use model-based conversion
            preset_data = self._parser.parse_file(input_path)
            gp5_preset = GP5Preset(
                name=preset_data.name or input_path.stem,
                version=preset_data.version or "1.0",
                parameters=preset_data.parameters,
            )
            gp50_preset: GP50Preset = self._core_converter.convert(gp5_preset)
            self._writer.write_gp50(gp50_preset, output_path)
            return output_path

        # Write output
        self._writer.write_binary(converted_data, output_path)

        return output_path

    def convert_directory(
        self,
        input_dir: Path,
        output_dir: Optional[Path] = None,
        target_format: Optional[str] = None,
    ) -> list[Path]:
        """
        Convert all .prst preset files in a directory.

        Args:
            input_dir: Directory containing preset files
            output_dir: Optional output directory
            target_format: Optional target format ("GP5" or "GP50")

        Returns:
            List of paths to converted preset files

        Raises:
            NotADirectoryError: If input_dir is not a directory
        """
        if not input_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {input_dir}")

        if output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)

        converted_files = []

        # Look for .prst files (real hardware format)
        preset_files = list(input_dir.glob("*.prst"))

        # Also look for legacy .gp5 files
        preset_files.extend(input_dir.glob("*.gp5"))

        for preset_file in sorted(preset_files):
            if output_dir:
                # Change extension based on target format for legacy files
                if preset_file.suffix == ".gp5":
                    output_path = output_dir / preset_file.with_suffix(".gp50").name
                elif preset_file.suffix == ".gp50":
                    output_path = output_dir / preset_file.with_suffix(".gp5").name
                else:
                    output_path = output_dir / preset_file.name
            else:
                output_path = None

            try:
                converted_path = self.convert_file(
                    preset_file, output_path, target_format
                )
                converted_files.append(converted_path)
            except (ValueError, AssertionError) as e:
                print(f"  Skipping {preset_file.name}: {e}")

        return converted_files

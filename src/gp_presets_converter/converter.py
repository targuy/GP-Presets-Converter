"""
Preset converter module for VALETON GP-5 / GP-50 bidirectional conversion.

This module handles the conversion logic between GP-5 and GP-50 .prst preset formats.
While the internal engine and modules are shared, the binary file structure differs.
"""

import re
from pathlib import Path
from typing import Optional

from .core.converter import CoreConverter
from .core.parser import PresetParser
from .core.writer import PresetWriter
from .models.gp5_preset import GP5Preset
from .models.gp50_preset import GP50Preset


def _parse_slot_from_filename(filename: str) -> Optional[int]:
    """
    Extract the leading slot number from a preset filename.

    E.g. "55-TimPierce.prst" -> 55, "myPreset.prst" -> None

    Args:
        filename: The filename (stem or with extension)

    Returns:
        The slot number or None if not present
    """
    stem = Path(filename).stem
    match = re.match(r"^(\d+)-", stem)
    if match:
        return int(match.group(1))
    return None


def _replace_slot_in_filename(filename: str, new_slot: int) -> str:
    """
    Replace the leading slot number in a preset filename.

    E.g. _replace_slot_in_filename("55-TimPierce.prst", 70) -> "70-TimPierce.prst"
    If the filename has no leading slot, prepend one:
    E.g. _replace_slot_in_filename("TimPierce.prst", 70) -> "70-TimPierce.prst"

    Args:
        filename: Original filename
        new_slot: New slot number

    Returns:
        Updated filename string
    """
    path = Path(filename)
    stem = path.stem
    suffix = path.suffix
    match = re.match(r"^\d+-(.*)", stem)
    if match:
        return f"{new_slot}-{match.group(1)}{suffix}"
    else:
        return f"{new_slot}-{stem}{suffix}"


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
        target_slot: Optional[int] = None,
        nam_offset: int = 0,
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
            target_slot: Optional target slot number. Changes the leading
                        number in the output filename (e.g. 55-Name.prst -> 70-Name.prst).
                        Must be 0-127. Does NOT modify binary data (slot lives in filename only).
            nam_offset: Signed integer offset to apply to the NAM/SnapTone
                       slot reference inside the binary data. Default 0 (no change).
                       Use when NAM models are loaded in different slots on source
                       vs target device.

        Returns:
            Path to the converted preset file

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input file is not a valid preset, or target_slot is out of range
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if target_slot is not None and (target_slot < 0 or target_slot > 127):
            raise ValueError(f"Target slot must be 0-127, got {target_slot}")

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
                output_name = input_path.name
                # Apply slot renaming if requested
                if target_slot is not None:
                    output_name = _replace_slot_in_filename(output_name, target_slot)
                output_path = input_path.parent / output_name
                if output_path == input_path:
                    stem = output_path.stem
                    output_path = input_path.parent / f"{stem}_{target_format.lower()}.prst"
            else:
                # Legacy format: use appropriate extension
                ext = ".gp50" if target_format == "GP50" else ".gp5"
                output_path = input_path.with_suffix(ext)
        elif target_slot is not None:
            # User provided explicit output_path AND target_slot:
            # apply slot renaming to the output filename
            output_name = _replace_slot_in_filename(output_path.name, target_slot)
            output_path = output_path.parent / output_name

        # Show NAM warning if converting real .prst and no nam_offset provided
        is_real_gp5 = data[:5] == b"GP-5\x00" and len(data) == 507
        is_real_gp50 = data[:5] == b"GP-50" and len(data) == 552

        nam_ref = CoreConverter.get_nam_ref(data)
        if (is_real_gp5 or is_real_gp50) and nam_ref > 0 and nam_offset == 0:
            print(
                f"  ⚠ NAM/SnapTone slot {nam_ref} referenced in preset. "
                f"Use --nam-offset if slots differ on target device."
            )

        print(f"Converting {input_path.name} ({detected_format} -> {target_format})")

        if is_real_gp5 and target_format == "GP50":
            converted_data = CoreConverter.convert_gp5_to_gp50(data, nam_offset=nam_offset)
        elif is_real_gp50 and target_format == "GP5":
            converted_data = CoreConverter.convert_gp50_to_gp5(data, nam_offset=nam_offset)
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
        start_slot: Optional[int] = None,
        nam_offset: int = 0,
    ) -> list[Path]:
        """
        Convert all .prst preset files in a directory.

        Args:
            input_dir: Directory containing preset files
            output_dir: Optional output directory
            target_format: Optional target format ("GP5" or "GP50")
            start_slot: Optional starting slot number for batch conversion.
                       Each successive file gets an incrementing slot number.
                       Must be 0-127.
            nam_offset: Signed integer offset for NAM/SnapTone slot remapping.

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

        current_slot = start_slot

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
                    preset_file,
                    output_path,
                    target_format,
                    target_slot=current_slot,
                    nam_offset=nam_offset,
                )
                converted_files.append(converted_path)

                if current_slot is not None:
                    current_slot += 1
                    if current_slot > 127:
                        print(
                            f"  ⚠ Slot number exceeded 127 after {preset_file.name}. "
                            f"Remaining files will not have slot numbers assigned."
                        )
                        current_slot = None
            except (ValueError, AssertionError) as e:
                print(f"  Skipping {preset_file.name}: {e}")

        return converted_files

"""
Preset converter module for VALETON GP-5 to GP-50 conversion.

This module handles the core conversion logic between GP-5 and GP-50 preset formats.
While the internal engine and modules are shared, the user interface and I/O ports differ.
"""

from pathlib import Path
from typing import Optional


class PresetConverter:
    """
    Convert VALETON GP-5 preset files to GP-50 format.

    The GP-5 and GP-50 share the same internal modules and architecture,
    but differ in user interface and input/output port configurations.
    """

    def __init__(self) -> None:
        """Initialize the preset converter."""
        self.version = "0.1.0"

    def convert_file(self, input_path: Path, output_path: Optional[Path] = None) -> Path:
        """
        Convert a GP-5 preset file to GP-50 format.

        Args:
            input_path: Path to the GP-5 preset file
            output_path: Optional path for the output file. If not provided,
                        generates output path based on input filename.

        Returns:
            Path to the converted GP-50 preset file

        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If input file is not a valid GP-5 preset
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        if output_path is None:
            output_path = input_path.with_suffix(".gp50")

        # TODO: Implement actual conversion logic
        # This is a placeholder for the conversion logic
        print(f"Converting {input_path} to {output_path}")

        return output_path

    def convert_directory(self, input_dir: Path, output_dir: Optional[Path] = None) -> list[Path]:
        """
        Convert all GP-5 preset files in a directory to GP-50 format.

        Args:
            input_dir: Directory containing GP-5 preset files
            output_dir: Optional output directory. If not provided,
                       files are saved alongside originals.

        Returns:
            List of paths to converted preset files

        Raises:
            NotADirectoryError: If input_dir is not a directory
        """
        if not input_dir.is_dir():
            raise NotADirectoryError(f"Not a directory: {input_dir}")

        converted_files = []

        # Look for GP-5 preset files (adjust extension as needed)
        for preset_file in input_dir.glob("*.gp5"):
            if output_dir:
                output_path = output_dir / preset_file.with_suffix(".gp50").name
            else:
                output_path = None

            converted_path = self.convert_file(preset_file, output_path)
            converted_files.append(converted_path)

        return converted_files

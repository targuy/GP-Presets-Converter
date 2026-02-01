"""
Output file writer for preset files.

This module handles writing converted presets to disk in the appropriate format.
"""

from pathlib import Path
from typing import Optional

from ..models.gp50_preset import GP50Preset
from ..utils.binary_parser import BinaryWriter


class PresetWriter:
    """
    Writer for VALETON preset files.

    Handles serialization of preset data structures to binary format
    and writing to disk.
    """

    def __init__(self) -> None:
        """Initialize the preset writer."""
        pass

    def write_gp50(self, preset: GP50Preset, output_path: Path) -> None:
        """
        Write a GP-50 preset to disk.

        Args:
            preset: GP50Preset object to write
            output_path: Path where the preset file should be written

        Raises:
            IOError: If file cannot be written
        """
        # Create binary data from preset
        writer = BinaryWriter()

        # Write signature
        writer.write_bytes(b"GP50")

        # Write version
        writer.write_string(preset.version, 16)

        # Write preset name
        writer.write_string(preset.name, 32)

        # Write parameters (placeholder structure)
        # This would be replaced with actual GP-50 binary format
        for key, value in preset.parameters.items():
            # Placeholder serialization
            pass

        # Get binary data
        data = writer.get_bytes()

        # Write to file
        self._write_file(output_path, data)

    def _write_file(self, path: Path, data: bytes) -> None:
        """
        Write binary data to file with proper error handling.

        Args:
            path: Path to write to
            data: Binary data to write

        Raises:
            IOError: If file cannot be written
        """
        try:
            # Create parent directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(path, "wb") as f:
                f.write(data)
        except Exception as e:
            raise IOError(f"Failed to write preset file: {e}") from e

    def create_backup(self, file_path: Path) -> Optional[Path]:
        """
        Create a backup of an existing preset file before overwriting.

        Args:
            file_path: Path to the file to backup

        Returns:
            Path to backup file if created, None if original doesn't exist
        """
        if not file_path.exists():
            return None

        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        counter = 1

        # Find unique backup filename
        while backup_path.exists():
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup{counter}")
            counter += 1

        # Copy original to backup
        import shutil

        shutil.copy2(file_path, backup_path)
        return backup_path

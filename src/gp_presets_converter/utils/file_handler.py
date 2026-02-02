"""
File I/O utilities for preset files.

This module provides utilities for reading, writing, and managing preset files.
"""

import shutil
from pathlib import Path
from typing import List, Optional


class FileHandler:
    """
    Utility class for handling preset file operations.

    Provides safe file operations with proper error handling and backup support.
    """

    @staticmethod
    def read_binary(file_path: Path) -> bytes:
        """
        Read binary data from a file.

        Args:
            file_path: Path to file to read

        Returns:
            Binary data from file

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            raise IOError(f"Failed to read file: {e}") from e

    @staticmethod
    def write_binary(file_path: Path, data: bytes, create_backup: bool = True) -> None:
        """
        Write binary data to a file.

        Args:
            file_path: Path to write to
            data: Binary data to write
            create_backup: Whether to create a backup of existing file

        Raises:
            IOError: If file cannot be written
        """
        try:
            # Create backup if file exists and backup is requested
            if create_backup and file_path.exists():
                FileHandler.create_backup(file_path)

            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(file_path, "wb") as f:
                f.write(data)
        except Exception as e:
            raise IOError(f"Failed to write file: {e}") from e

    @staticmethod
    def create_backup(file_path: Path) -> Path:
        """
        Create a backup of a file.

        Args:
            file_path: Path to file to backup

        Returns:
            Path to backup file

        Raises:
            FileNotFoundError: If source file doesn't exist
            IOError: If backup cannot be created
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Cannot backup non-existent file: {file_path}")

        backup_path = file_path.with_suffix(file_path.suffix + ".backup")
        counter = 1

        # Find unique backup filename
        while backup_path.exists():
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup{counter}")
            counter += 1

        try:
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception as e:
            raise IOError(f"Failed to create backup: {e}") from e

    @staticmethod
    def find_preset_files(
        directory: Path, extensions: Optional[List[str]] = None
    ) -> List[Path]:
        """
        Find all preset files in a directory.

        Args:
            directory: Directory to search
            extensions: List of file extensions to search for (e.g., ['.gp5', '.gp50'])
                       If None, searches for common preset extensions

        Returns:
            List of paths to preset files

        Raises:
            NotADirectoryError: If path is not a directory
        """
        if not directory.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory}")

        if extensions is None:
            extensions = [".gp5", ".gp50", ".preset"]

        preset_files = []
        for ext in extensions:
            preset_files.extend(directory.glob(f"*{ext}"))
            preset_files.extend(directory.glob(f"**/*{ext}"))  # Recursive search

        # Remove duplicates and sort
        return sorted(set(preset_files))

    @staticmethod
    def ensure_directory(directory: Path) -> None:
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            directory: Path to directory

        Raises:
            IOError: If directory cannot be created
        """
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise IOError(f"Failed to create directory: {e}") from e

    @staticmethod
    def get_file_size(file_path: Path) -> int:
        """
        Get the size of a file in bytes.

        Args:
            file_path: Path to file

        Returns:
            File size in bytes

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return file_path.stat().st_size

    @staticmethod
    def is_valid_preset_file(file_path: Path, min_size: int = 0, max_size: int = 10 * 1024 * 1024) -> bool:
        """
        Check if a file is likely a valid preset file based on basic criteria.

        Args:
            file_path: Path to file to check
            min_size: Minimum valid file size in bytes
            max_size: Maximum valid file size in bytes

        Returns:
            True if file appears to be a valid preset file
        """
        if not file_path.exists() or not file_path.is_file():
            return False

        try:
            size = FileHandler.get_file_size(file_path)
            return min_size <= size <= max_size
        except Exception:
            return False

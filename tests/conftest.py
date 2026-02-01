"""
Pytest configuration and shared fixtures.

This file contains test configuration and fixtures shared across all test modules.
"""

import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """
    Create a temporary directory for test files.

    Yields:
        Path: Path to temporary directory

    The directory is automatically cleaned up after the test.
    """
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_gp5_data():
    """
    Create sample GP-5 preset binary data for testing.

    Returns:
        bytes: Sample GP-5 preset data
    """
    import struct

    data = bytearray()

    # Magic signature
    data.extend(b'GP5\x00')

    # Version
    data.extend(struct.pack('<H', 1))

    # Preset name (32 bytes)
    name = b'Test Preset\x00' + b'\x00' * 20
    data.extend(name[:32])

    # Some parameters
    for i in range(10):
        data.extend(struct.pack('<H', i * 10))

    # Padding
    data.extend(b'\x00' * 100)

    return bytes(data)


@pytest.fixture
def sample_gp50_data():
    """
    Create sample GP-50 preset binary data for testing.

    Returns:
        bytes: Sample GP-50 preset data
    """
    import struct

    data = bytearray()

    # Magic signature
    data.extend(b'GP50')

    # Version
    data.extend(struct.pack('<H', 1))

    # Preset name (32 bytes)
    name = b'Test GP50 Preset\x00' + b'\x00' * 15
    data.extend(name[:32])

    # Some parameters
    for i in range(12):
        data.extend(struct.pack('<H', i * 10))

    # Padding
    data.extend(b'\x00' * 100)

    return bytes(data)


@pytest.fixture
def sample_gp5_file(temp_dir, sample_gp5_data):
    """
    Create a sample GP-5 preset file for testing.

    Args:
        temp_dir: Temporary directory fixture
        sample_gp5_data: Sample GP-5 data fixture

    Returns:
        Path: Path to created GP-5 file
    """
    file_path = temp_dir / "test_preset.gp5"
    file_path.write_bytes(sample_gp5_data)
    return file_path


@pytest.fixture
def sample_gp50_file(temp_dir, sample_gp50_data):
    """
    Create a sample GP-50 preset file for testing.

    Args:
        temp_dir: Temporary directory fixture
        sample_gp50_data: Sample GP-50 data fixture

    Returns:
        Path: Path to created GP-50 file
    """
    file_path = temp_dir / "test_preset.gp50"
    file_path.write_bytes(sample_gp50_data)
    return file_path


@pytest.fixture
def multiple_gp5_files(temp_dir, sample_gp5_data):
    """
    Create multiple GP-5 preset files for batch testing.

    Args:
        temp_dir: Temporary directory fixture
        sample_gp5_data: Sample GP-5 data fixture

    Returns:
        list[Path]: List of created GP-5 file paths
    """
    files = []
    for i in range(5):
        file_path = temp_dir / f"preset_{i}.gp5"
        file_path.write_bytes(sample_gp5_data)
        files.append(file_path)
    return files


@pytest.fixture
def corrupted_file(temp_dir):
    """
    Create a corrupted file for error testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to corrupted file
    """
    file_path = temp_dir / "corrupted.preset"
    file_path.write_bytes(b'\xFF' * 10)  # Invalid data
    return file_path


@pytest.fixture
def empty_file(temp_dir):
    """
    Create an empty file for error testing.

    Args:
        temp_dir: Temporary directory fixture

    Returns:
        Path: Path to empty file
    """
    file_path = temp_dir / "empty.preset"
    file_path.write_bytes(b'')
    return file_path


# Test configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

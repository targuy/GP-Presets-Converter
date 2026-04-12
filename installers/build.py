#!/usr/bin/env python3
"""
Cross-platform build script for GP Presets Converter standalone executable.

Usage:
    python installers/build.py

Requires PyInstaller:
    pip install pyinstaller
"""

import platform
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Build the standalone executable using PyInstaller."""
    # Locate project root (parent of installers/)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    entry_point = project_root / "src" / "gp_presets_converter" / "cli.py"

    if not entry_point.exists():
        print(f"Error: entry point not found at {entry_point}", file=sys.stderr)
        return 1

    # Check PyInstaller is available
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("Error: PyInstaller is not installed. Run: pip install pyinstaller", file=sys.stderr)
        return 1

    system = platform.system()
    print(f"Building for {system} ({platform.machine()})...")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        "gp-convert",
        "--distpath",
        str(project_root / "dist"),
        "--workpath",
        str(project_root / "build" / "pyinstaller"),
        "--specpath",
        str(project_root / "build"),
        # Add the src directory to the Python path
        "--paths",
        str(project_root / "src"),
        str(entry_point),
    ]

    # macOS-specific: don't create a .app bundle, just a CLI binary
    if system == "Darwin":
        cmd.insert(4, "--console")

    # Windows-specific: console application (not windowed)
    if system == "Windows":
        cmd.insert(4, "--console")

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(project_root))

    if result.returncode == 0:
        exe_name = "gp-convert.exe" if system == "Windows" else "gp-convert"
        exe_path = project_root / "dist" / exe_name
        print(f"\n✓ Build successful: {exe_path}")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"  Size: {size_mb:.1f} MB")
    else:
        print("\n✗ Build failed", file=sys.stderr)

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())

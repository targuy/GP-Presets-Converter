#!/bin/bash
# Build standalone macOS executable for GP Presets Converter
# Requires: pip install pyinstaller
# Output:   dist/gp-convert

set -e

echo "=========================================="
echo "GP Presets Converter - macOS Build"
echo "=========================================="
echo ""

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Using Python: $(python3 --version)"

# Check/install PyInstaller
if ! python3 -c "import PyInstaller" &>/dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

echo "Building standalone executable..."
python3 -m PyInstaller \
    --onefile \
    --console \
    --name gp-convert \
    --distpath dist \
    --workpath build/pyinstaller \
    --specpath build \
    --paths src \
    src/gp_presets_converter/cli.py

echo ""
echo "=========================================="
echo "Build successful!"
echo "Executable: dist/gp-convert"
echo "=========================================="
echo ""
echo "Installation:"
echo "  cp dist/gp-convert /usr/local/bin/"
echo ""
echo "Usage:"
echo "  gp-convert 55-TimPierce.prst --slot 70"
echo "  gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60"
echo ""
echo "If macOS Gatekeeper blocks the app:"
echo "  xattr -d com.apple.quarantine dist/gp-convert"

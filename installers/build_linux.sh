#!/bin/bash
# Build standalone Linux executable for GP Presets Converter
# Requires: pip install pyinstaller
# Output:   dist/gp-convert

set -e

echo "=========================================="
echo "GP Presets Converter - Linux Build"
echo "=========================================="
echo ""

# Navigate to project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Install with: sudo apt-get install python3 python3-pip python3-venv"
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
    --name gp-convert \
    --distpath dist \
    --workpath build/pyinstaller \
    --specpath build \
    --paths src \
    src/gp_presets_converter/cli.py

# Make executable
chmod +x dist/gp-convert

echo ""
echo "=========================================="
echo "Build successful!"
echo "Executable: dist/gp-convert"
echo "=========================================="
echo ""
echo "Installation:"
echo "  # System-wide:"
echo "  sudo cp dist/gp-convert /usr/local/bin/"
echo ""
echo "  # User-only:"
echo "  mkdir -p ~/.local/bin"
echo "  cp dist/gp-convert ~/.local/bin/"
echo "  # Make sure ~/.local/bin is in your PATH"
echo ""
echo "Usage:"
echo "  gp-convert 55-TimPierce.prst --slot 70"
echo "  gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60"

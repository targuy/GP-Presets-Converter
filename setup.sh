#!/bin/bash

# Setup script for GP Presets Converter development environment

set -e

echo "=========================================="
echo "GP Presets Converter - Environment Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"

REQUIRED_VERSION="3.12"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)"; then
    echo "Error: Python 3.12 or higher is required"
    echo "Please install Python 3.12+ and try again"
    exit 1
fi

echo "✓ Python version check passed"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install development dependencies
echo "Installing development dependencies..."
pip install -e '.[dev]'
echo "✓ Dependencies installed"
echo ""

# Run tests to verify installation
echo "Running tests to verify installation..."
pytest tests/ -v
echo "✓ Tests passed"
echo ""

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"
echo ""
echo "Available make commands:"
echo "  make test         - Run tests"
echo "  make lint         - Run linters"
echo "  make format       - Format code"
echo "  make clean        - Clean build artifacts"
echo ""
echo "Happy coding!"

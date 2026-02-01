# Installation Guide

This guide covers installing the GP Presets Converter on various platforms and for different use cases.

## Requirements

- Python 3.12 or higher
- pip package manager

## Installation Methods

### For End Users

Install the package using pip:

```bash
pip install -e .
```

This installs the converter in editable mode, allowing you to update it by pulling changes from git.

### For Developers

1. **Clone the repository:**

```bash
git clone https://github.com/targuy/GP-Presets-Converter.git
cd GP-Presets-Converter
```

2. **Create a virtual environment (recommended):**

```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode with dev dependencies:**

```bash
pip install -e '.[dev]'
```

Or use the Makefile:

```bash
make install-dev
```

### Using GitHub Codespaces

The repository is configured for GitHub Codespaces:

1. Click "Code" → "Create codespace on main"
2. Wait for the environment to set up automatically
3. Start developing immediately

The dev container includes:
- Python 3.12
- All dependencies pre-installed
- VSCode extensions configured

### Using Docker (Alternative)

If you prefer Docker:

```bash
docker build -t gp-presets-converter .
docker run -v $(pwd)/presets:/presets gp-presets-converter convert /presets/input.gp5
```

## Verifying Installation

After installation, verify it works:

```bash
# Check version
gp-convert --version

# Run tests
pytest tests/

# Try the CLI
gp-convert --help
```

## Updating

### End Users

```bash
cd GP-Presets-Converter
git pull
pip install -e .
```

### Developers

```bash
cd GP-Presets-Converter
git pull
pip install -e '.[dev]'
```

## Troubleshooting Installation

### Python Version Issues

If you get a Python version error:

```bash
# Check your Python version
python --version

# If below 3.12, install Python 3.12
# On Ubuntu/Debian:
sudo apt-get install python3.12 python3.12-venv

# On macOS with Homebrew:
brew install python@3.12
```

### Permission Errors

If you encounter permission errors:

```bash
# Use --user flag
pip install --user -e .

# Or use a virtual environment (recommended)
python3.12 -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
```

### Missing Dependencies

If dependencies fail to install:

```bash
# Update pip
pip install --upgrade pip setuptools wheel

# Try installing again
pip install -e '.[dev]'
```

### Build Errors

If you encounter build errors:

```bash
# Install build essentials
# On Ubuntu/Debian:
sudo apt-get install build-essential python3.12-dev

# On macOS:
xcode-select --install
```

## Platform-Specific Notes

### Windows

- Use PowerShell or Windows Terminal
- Virtual environment activation: `venv\Scripts\activate`
- Some commands may require `py` instead of `python`

### macOS

- May need to use `python3` instead of `python`
- If using Homebrew Python, ensure it's in your PATH

### Linux

- Ensure Python 3.12 is installed from your distribution's repositories
- May need to install `python3.12-venv` separately

## Optional Dependencies

For development, you may want additional tools:

```bash
# Code formatters and linters (included in dev dependencies)
pip install black flake8 mypy isort

# Documentation generation
pip install sphinx sphinx-rtd-theme

# Pre-commit hooks
pip install pre-commit
pre-commit install
```

## Uninstalling

To remove the package:

```bash
pip uninstall gp-presets-converter
```

To completely clean up:

```bash
# Remove the virtual environment
rm -rf venv/

# Remove build artifacts
make clean

# Or manually:
rm -rf build/ dist/ *.egg-info .pytest_cache .mypy_cache
```

## Next Steps

After installation:

1. Read the [Usage Guide](usage.md) to learn how to use the converter
2. Check out the [Examples](../examples/README.md) directory
3. Review the [API Reference](api_reference.md) for programmatic usage

## Getting Help

If you encounter issues during installation:

1. Check the [Troubleshooting Guide](troubleshooting.md)
2. Search existing [GitHub Issues](https://github.com/targuy/GP-Presets-Converter/issues)
3. Create a new issue with:
   - Your operating system and version
   - Python version (`python --version`)
   - Full error message
   - Installation method you used

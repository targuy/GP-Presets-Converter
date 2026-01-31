# GP Presets Converter

Convert VALETON GP-5 preset files to GP-50 format.

## Overview

This Python project provides tools to convert preset files between VALETON multi-effects pedal formats. The GP-5 and GP-50 share the same internal modules and architecture, but differ in user interface and input/output port configurations.

## Features

- Convert individual GP-5 preset files to GP-50 format
- Batch convert entire directories of preset files
- Command-line interface for easy usage
- Python API for programmatic access

## Requirements

- Python 3.12 or higher

## Installation

### For Users

```bash
pip install -e .
```

### For Developers

1. Clone the repository:
```bash
git clone https://github.com/targuy/GP-Presets-Converter.git
cd GP-Presets-Converter
```

2. Create a virtual environment:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e '.[dev]'
```

Or use the Makefile:
```bash
make install-dev
```

## Usage

### Command Line

Convert a single file:
```bash
gp-convert input.gp5 -o output.gp50
```

Convert all files in a directory:
```bash
gp-convert /path/to/presets/ -o /path/to/output/
```

### Python API

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
converter.convert_file(Path("input.gp5"), Path("output.gp50"))
```

## Development

### Running Tests

```bash
make test
```

Or directly with pytest:
```bash
pytest tests/ -v
```

### Code Formatting

```bash
make format
```

### Linting

```bash
make lint
```

### VSCode Setup

This project is configured for VSCode with:
- Python extension settings
- Debugging configurations
- Testing integration
- Auto-formatting on save

Simply open the project in VSCode and the settings will be applied automatically.

### GitHub Codespaces

This project is ready to use with GitHub Codespaces. The dev container will automatically:
- Set up Python 3.12
- Install all dependencies
- Configure VSCode extensions

Click "Code" → "Create codespace on main" to get started.

## Project Structure

```
GP-Presets-Converter/
├── src/
│   └── gp_presets_converter/
│       ├── __init__.py
│       ├── converter.py       # Core conversion logic
│       └── cli.py            # Command-line interface
├── tests/
│   ├── __init__.py
│   └── test_converter.py     # Test suite
├── .vscode/                  # VSCode configuration
├── .devcontainer/            # Codespaces configuration
├── pyproject.toml            # Project metadata and dependencies
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── Makefile                  # Development commands
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Authors

GP Presets Converter Contributors

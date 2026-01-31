# GP Presets Converter

Convert VALETON GP-5 preset files to GP-50 format.

## Overview

This Python project provides tools to convert preset files between VALETON multi-effects pedal formats. The GP-5 and GP-50 share the same internal modules and architecture, but differ in user interface and input/output port configurations.

## Features

- **Single File Conversion** - Convert individual GP-5 preset files to GP-50 format
- **Batch Processing** - Convert entire directories of preset files at once
- **Binary Analysis** - Analyze unknown preset file formats with hex dump tools
- **Command-Line Interface** - Easy-to-use CLI for common operations
- **Python API** - Full programmatic access for custom workflows
- **Extensible Architecture** - Easy to add support for additional formats

## Quick Start

### Installation

```bash
# For users
pip install -e .

# For developers
pip install -e '.[dev]'
```

### Basic Usage

```bash
# Convert a single file
gp-convert input.gp5 -o output.gp50

# Convert all files in a directory
gp-convert ./gp5_presets/ -o ./gp50_presets/ -v

# Analyze a preset file format
gp-convert input.gp5 --analyze

# Get help
gp-convert --help
```

### Python API

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
converter.convert_file(Path("input.gp5"), Path("output.gp50"))
```

## Documentation

Comprehensive documentation is available in the [docs/](docs/) directory:

- **[Installation Guide](docs/installation.md)** - How to install on various platforms
- **[Usage Guide](docs/usage.md)** - Detailed usage examples and workflows
- **[API Reference](docs/api_reference.md)** - Complete API documentation
- **[Preset Format Analysis](docs/preset_format_analysis.md)** - Understanding preset file formats
- **[Conversion Guide](docs/conversion_guide.md)** - Step-by-step conversion process
- **[Development Guide](docs/development.md)** - Contributing and development guidelines
- **[Troubleshooting](docs/troubleshooting.md)** - Common issues and solutions

## Examples

The [examples/](examples/) directory contains:

- **Sample Preset Files** - GP-5 and GP-50 preset examples
- **Usage Examples** - Python scripts demonstrating various features
- **Format Analysis** - Tools and documentation for analyzing binary formats
- **Test Files** - Small preset files for testing

## Project Structure

```
GP-Presets-Converter/
├── src/gp_presets_converter/    # Main package
│   ├── core/                    # Core conversion logic
│   │   ├── analyzer.py          # Binary file analysis
│   │   ├── converter.py         # Format conversion
│   │   ├── parser.py            # Preset file parser
│   │   └── writer.py            # Output file writer
│   ├── models/                  # Data models
│   │   ├── gp5_preset.py        # GP-5 preset model
│   │   ├── gp50_preset.py       # GP-50 preset model
│   │   ├── preset.py            # Base preset class
│   │   └── common.py            # Common data structures
│   ├── utils/                   # Utility functions
│   │   ├── binary_parser.py     # Binary data parsing
│   │   ├── file_handler.py      # File I/O utilities
│   │   ├── hex_dump.py          # Hex dump tools
│   │   └── validation.py        # Data validation
│   ├── config/                  # Configuration
│   │   └── settings.py          # Settings and constants
│   ├── cli.py                   # Command-line interface
│   └── converter.py             # Main converter class
├── tests/                       # Test suite (58 tests)
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── conftest.py              # Pytest fixtures
├── examples/                    # Usage examples
│   ├── usage_examples/          # Python example scripts
│   ├── valeton_presets/         # Sample preset files
│   └── test_files/              # Test preset files
├── docs/                        # Documentation (8 guides)
└── pyproject.toml               # Project configuration
```

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=gp_presets_converter

# Run specific test
pytest tests/unit/test_parser.py -v
```

### Code Formatting

```bash
# Format code
make format

# Or manually
black src/gp_presets_converter tests/
isort src/gp_presets_converter tests/
```

### Linting

```bash
# Run linters
make lint

# Or manually
flake8 src/gp_presets_converter tests/
mypy src/gp_presets_converter
```

## Requirements

- Python 3.12 or higher
- See [requirements.txt](requirements.txt) for runtime dependencies
- See [requirements-dev.txt](requirements-dev.txt) for development dependencies

## Architecture

The converter uses a modular architecture:

1. **Parser** - Reads binary preset files and extracts parameters
2. **Converter** - Translates GP-5 parameters to GP-50 format
3. **Writer** - Writes converted data to GP-50 binary format
4. **Analyzer** - Provides tools for understanding unknown formats

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and the [Development Guide](docs/development.md) for details.

### Areas for Contribution

- **Format Analysis** - Help reverse-engineer preset file formats
- **Testing** - Add test cases and improve coverage
- **Documentation** - Improve guides and examples
- **Features** - Add support for new devices or formats
- **Bug Fixes** - Report and fix issues

## Testing Status

- **58 Tests Passing** - Comprehensive unit and integration tests
- **58% Code Coverage** - Good coverage of core functionality
- **Continuous Testing** - Automated test execution

## VSCode Integration

This project is configured for VSCode with:
- Python extension settings
- Debugging configurations
- Testing integration
- Auto-formatting on save

Simply open the project in VSCode for full IDE support.

## GitHub Codespaces

Click "Code" → "Create codespace on main" for an instant development environment with:
- Python 3.12 pre-installed
- All dependencies configured
- VSCode extensions ready
- Zero local setup required

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Authors

GP Presets Converter Contributors

## Support

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Report bugs on [GitHub Issues](https://github.com/targuy/GP-Presets-Converter/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/targuy/GP-Presets-Converter/discussions)

## Acknowledgments

- VALETON for creating the GP-5 and GP-50 multi-effects pedals
- The open-source community for inspiration and tools

## Disclaimer

This project is not affiliated with VALETON. It is an independent community effort to provide interoperability tools for VALETON products. All analysis is performed on user-provided preset files for interoperability purposes.

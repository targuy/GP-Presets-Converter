# GP Presets Converter

Bidirectional converter between VALETON GP-5 and GP-50 `.prst` preset formats.

> Status / limitations (important)
> - Décodage partiel seulement : on extrait aujourd’hui le nom du preset, le slot NAM/SnapTone, quelques champs simples (volume, amp model id, ordre de chaîne). Les paramètres détaillés des modules FX et leurs états on/off ne sont pas encore cartographiés.
> - Conversion testée sur un petit jeu d’exemples ; d’autres packs peuvent nécessiter `--nam-offset` ou un réglage manuel dans Valeton Suite.
> - Si vous devez inspecter rapidement vos presets, utilisez `--export-json` pour générer un inventaire lisible (nom, format, slot NAM, paramètres basiques).

## Overview

This Python project provides tools to convert preset files bidirectionally between VALETON GP-5 and GP-50 multi-effects pedal formats. The GP-5 and GP-50 share the same internal modules and architecture, but differ in binary layout (507 vs 552 bytes), mixer section size, and device type tags. Conversion is fully automatic — the tool auto-detects the source format and converts to the opposite device.

## Features

- **Bidirectional Conversion** - Convert GP-5 → GP-50 and GP-50 → GP-5 (auto-detected)
- **Batch Processing** - Convert entire directories of `.prst` files at once
- **Slot Management** - `--slot N` sets the target slot number (0–127) in the output filename; sequential numbering for batch runs
- **NAM/SnapTone Offset** - `--nam-offset N` remaps NAM/SnapTone slot references when models live in different slots on source vs target device
- **NAM Warning** - Automatic warning when a preset references a NAM/SnapTone slot and no `--nam-offset` is specified
- **Binary Analysis** - Analyze preset file formats with hex dump tools
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
# Basic conversion (auto-detects direction)
gp-convert 55-TimPierce.prst

# Set target slot
gp-convert 55-TimPierce.prst --slot 70

# Batch convert with sequential slots starting at 60
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60

# Remap NAM references (shift by +5)
gp-convert 55-TimPierce.prst --nam-offset 5

# Explicit target format
gp-convert preset.prst -t GP50

# Analyze a preset file
gp-convert preset.prst --analyze

# Export readable metadata (no conversion)
gp-convert ./GP5_PRESETS/ --export-json presets_meta.json

# Get help
gp-convert --help
```

### Python API

```python
from pathlib import Path
from gp_presets_converter import PresetConverter
from gp_presets_converter.core.converter import CoreConverter

converter = PresetConverter()

# Single file with slot and NAM offset
converter.convert_file(
    Path("55-TimPierce.prst"),
    target_slot=70,
    nam_offset=5,
)

# Batch with sequential slots
converter.convert_directory(
    Path("./GP5_PRESETS/"),
    Path("./GP50_PRESETS/"),
    start_slot=60,
    nam_offset=5,
)

# Binary-level
gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data, nam_offset=5)
gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data, nam_offset=-5)
nam_ref = CoreConverter.get_nam_ref(data)
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
├── tests/                       # Test suite (666 tests)
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

1. **Parser** - Reads binary `.prst` files and detects GP-5 vs GP-50 format
2. **CoreConverter** - Bidirectional binary conversion between GP-5 (507 bytes) and GP-50 (552 bytes)
3. **Writer** - Writes converted data to the target binary format
4. **Analyzer** - Provides tools for understanding preset formats
5. **Slot/NAM utilities** - Filename-based slot management and NAM reference remapping

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) and the [Development Guide](docs/development.md) for details.

### Areas for Contribution

- **Format Analysis** - Help reverse-engineer preset file formats
- **Testing** - Add test cases and improve coverage
- **Documentation** - Improve guides and examples
- **Features** - Add support for new devices or formats
- **Bug Fixes** - Report and fix issues

## Slot and NAM Management

### Slot Numbers

The preset slot number (0–127) is stored **only in the filename prefix** (e.g., `55-TimPierce.prst` → slot 55). It is not embedded in the binary data. Use `--slot N` to control where the converted preset lands on the target device.

For batch conversions, `--slot N` sets the starting slot and files are numbered sequentially from there.

### NAM/SnapTone References

Both devices support VALETON's NAM/SnapTone amp models loaded into user slots. The NAM slot reference is stored inside the binary at offset `0xA7` (GP-5) / `0xD2` (GP-50) as a tag `0x0c` value byte. A value of `0` means no NAM is assigned (built-in amp only).

If your NAM models are loaded in different slots on the source and target devices, use `--nam-offset N` to shift the reference. For example, if a preset references NAM slot 52 on GP-5 and you loaded that model into slot 57 on GP-50, use `--nam-offset 5`.

When a preset contains a NAM reference and `--nam-offset` is not specified, the converter prints a warning so you can verify the reference is correct.

## Testing Status

- **666 Tests Passing** - Comprehensive unit and integration tests
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

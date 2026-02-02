# GP Presets Converter Documentation

Welcome to the GP Presets Converter documentation. This tool converts VALETON GP-5 preset files to GP-50 format.

## Documentation Contents

- **[Installation Guide](installation.md)** - How to install and set up the converter
- **[Usage Guide](usage.md)** - Basic and advanced usage examples
- **[API Reference](api_reference.md)** - Complete API documentation
- **[Preset Format Analysis](preset_format_analysis.md)** - Understanding VALETON preset file formats
- **[Conversion Guide](conversion_guide.md)** - Detailed conversion process explanation
- **[Development Guide](development.md)** - Contributing and developing
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```bash
# Convert a single file
gp-convert input.gp5 -o output.gp50

# Convert a directory
gp-convert ./gp5_presets/ -o ./gp50_presets/ -v
```

### Python API

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
converter.convert_file(Path("input.gp5"), Path("output.gp50"))
```

## Project Overview

The GP Presets Converter is a Python tool designed to convert preset files between VALETON multi-effects pedal formats. The GP-5 and GP-50 share the same internal modules and architecture but differ in user interface and I/O port configurations.

### Key Features

- **Single File Conversion**: Convert individual preset files
- **Batch Processing**: Convert entire directories at once
- **Binary Analysis**: Tools for understanding preset file formats
- **Extensible Architecture**: Easy to add support for new formats
- **Comprehensive Testing**: Full test coverage
- **Type-Safe**: Full type hints throughout

### Architecture

The converter is organized into several packages:

- **core**: Core conversion and analysis logic
- **models**: Data structures for preset representation
- **utils**: Utility functions for file handling and validation
- **config**: Configuration and settings
- **cli**: Command-line interface

## Getting Help

- Check the [Troubleshooting Guide](troubleshooting.md) for common issues
- See [Usage Guide](usage.md) for detailed examples
- Review [API Reference](api_reference.md) for programmatic usage
- Visit the [GitHub Repository](https://github.com/targuy/GP-Presets-Converter) to report issues

## Contributing

We welcome contributions! See the [Development Guide](development.md) for information on:

- Setting up a development environment
- Code style guidelines
- Testing requirements
- Submitting pull requests

## License

This project is licensed under the MIT License. See the LICENSE file for details.

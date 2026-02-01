# Examples Directory

This directory contains example preset files, usage examples, and analysis tools for the GP Presets Converter.

## Directory Structure

```
examples/
├── README.md                          # This file
├── valeton_presets/                   # Preset file collection
│   ├── README.md                      # How to add and organize presets
│   ├── gp5/                           # GP-5 preset files
│   │   ├── README.md                  # GP-5 format notes
│   │   ├── factory/                   # Factory presets
│   │   ├── user/                      # User presets
│   │   └── community/                 # Community-contributed presets
│   ├── gp50/                          # GP-50 preset files
│   │   ├── README.md                  # GP-50 format notes
│   │   ├── factory/                   # Factory presets
│   │   ├── user/                      # User presets
│   │   └── community/                 # Community-contributed presets
│   └── analysis/                      # Analysis results
│       ├── README.md                  # Analysis documentation
│       ├── format_notes.md            # Format analysis notes
│       └── hex_dumps/                 # Hex dump files
├── usage_examples/                    # Python usage examples
│   ├── basic_conversion.py            # Simple file conversion
│   ├── batch_conversion.py            # Batch directory conversion
│   └── format_analysis.py             # Binary format analysis
└── test_files/                        # Small test files
    ├── simple_gp5.preset               # Simple GP-5 test file
    └── simple_gp50.preset              # Simple GP-50 test file
```

## Quick Start

### Converting a Single File

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
input_file = Path("examples/valeton_presets/gp5/factory/preset1.gp5")
output_file = Path("output/preset1.gp50")
converter.convert_file(input_file, output_file)
```

### Batch Converting Directory

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
input_dir = Path("examples/valeton_presets/gp5/user/")
output_dir = Path("output/gp50/")
converted = converter.convert_directory(input_dir, output_dir)
print(f"Converted {len(converted)} presets")
```

### Analyzing Binary Format

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
file_path = Path("examples/test_files/simple_gp5.preset")
analysis = analyzer.analyze_file(file_path)

print(f"File Size: {analysis['file_size']} bytes")
print(f"Signature: {analysis['signature']}")
print(f"Detected Strings: {analysis['possible_strings']}")
```

## Usage Examples

See the `usage_examples/` directory for detailed Python scripts demonstrating:

- **basic_conversion.py**: Simple single-file conversion
- **batch_conversion.py**: Converting entire directories with progress tracking
- **format_analysis.py**: Analyzing unknown preset file formats

## Contributing Presets

If you have VALETON GP-5 or GP-50 preset files that you'd like to contribute as examples:

1. Ensure you have the rights to share the presets
2. Add them to the appropriate directory:
   - Factory presets → `valeton_presets/gp5/factory/` or `valeton_presets/gp50/factory/`
   - Your own presets → `valeton_presets/gp5/user/` or `valeton_presets/gp50/user/`
   - Community presets → `valeton_presets/gp5/community/` or `valeton_presets/gp50/community/`
3. Include a brief description of the preset
4. Submit a pull request

Your contributions help improve the converter for everyone!

## Testing

The test files in `test_files/` are used for automated testing and format analysis.
These are small, well-understood preset files that demonstrate specific features.

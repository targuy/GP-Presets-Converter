# GP Presets Converter Examples

This directory contains example usage of the GP Presets Converter.

## Basic Usage

### Convert a Single File

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

# Initialize converter
converter = PresetConverter()

# Convert a GP-5 preset to GP-50 format
input_file = Path("my_preset.gp5")
output_file = Path("my_preset.gp50")

result = converter.convert_file(input_file, output_file)
print(f"Converted: {result}")
```

### Convert a Directory

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

# Initialize converter
converter = PresetConverter()

# Convert all GP-5 presets in a directory
input_dir = Path("./gp5_presets/")
output_dir = Path("./gp50_presets/")

# Create output directory if it doesn't exist
output_dir.mkdir(exist_ok=True)

# Convert all files
converted_files = converter.convert_directory(input_dir, output_dir)

print(f"Converted {len(converted_files)} files:")
for file in converted_files:
    print(f"  - {file.name}")
```

## Command Line Usage

### Convert a single file

```bash
gp-convert input.gp5 -o output.gp50
```

### Convert all files in a directory

```bash
gp-convert ./gp5_presets/ -o ./gp50_presets/ -v
```

### Get help

```bash
gp-convert --help
```

## Notes

- The GP-5 and GP-50 share the same internal modules and architecture
- Differences are mainly in user interface and I/O port configurations
- The converter handles these differences automatically

## Development

To implement actual conversion logic, edit `src/gp_presets_converter/converter.py`
and implement the file format parsing and conversion logic.

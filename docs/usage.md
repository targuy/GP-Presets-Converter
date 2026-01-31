# Usage Guide

This guide covers basic and advanced usage of the GP Presets Converter.

## Command-Line Interface

### Basic Commands

**Convert a single file:**
```bash
gp-convert input.gp5 -o output.gp50
```

**Convert a directory:**
```bash
gp-convert ./gp5_presets/ -o ./gp50_presets/
```

**Verbose output:**
```bash
gp-convert input.gp5 -o output.gp50 -v
```

**Check version:**
```bash
gp-convert --version
```

**Get help:**
```bash
gp-convert --help
```

### Advanced CLI Usage

**Batch conversion with pattern matching:**
```bash
# Convert all .gp5 files in a directory
gp-convert ./presets/*.gp5 -o ./converted/
```

## Python API

### Basic Usage

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

# Initialize converter
converter = PresetConverter()

# Convert single file
input_file = Path("my_preset.gp5")
output_file = Path("my_preset.gp50")
result = converter.convert_file(input_file, output_file)

print(f"Converted to: {result}")
```

### Batch Conversion

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()

# Convert all files in a directory
input_dir = Path("./gp5_presets/")
output_dir = Path("./gp50_presets/")

converted = converter.convert_directory(input_dir, output_dir)
print(f"Converted {len(converted)} files")
```

### Binary Analysis

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Analyze file structure
analysis = analyzer.analyze_file(Path("preset.gp5"))

print(f"File size: {analysis['file_size']} bytes")
print(f"Signature: {analysis['signature']}")
print(f"Strings: {analysis['possible_strings']}")
```

### File Comparison

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Compare two preset files
comparison = analyzer.compare_files(
    Path("preset1.gp5"),
    Path("preset2.gp5")
)

print(f"Similarity: {comparison['similarity_percentage']:.1f}%")
print(f"Differences: {comparison['byte_differences']}")
```

### Working with Preset Models

```python
from gp_presets_converter.models import GP5Preset, GP50Preset

# Create a GP-5 preset
gp5 = GP5Preset(
    name="My Preset",
    version="1.0",
    parameters={
        "input_gain": 75,
        "output_level": 80,
        "effects_chain": []
    }
)

# Validate preset
is_valid, errors = gp5.validate()
if not is_valid:
    print(f"Errors: {errors}")

# Add an effect
gp5.add_effect({
    "type": "overdrive",
    "drive": 60,
    "tone": 50,
    "level": 70
})
```

### Custom Settings

```python
from gp_presets_converter.config import Settings

# Create custom settings
settings = Settings()
settings.CREATE_BACKUP = True
settings.VERBOSE = True
settings.VALIDATE_OUTPUT = True

# Use with converter
# Note: Settings integration would need to be implemented in PresetConverter
```

## Examples

See the [examples directory](../examples/README.md) for complete working examples:

- **basic_conversion.py** - Simple file conversion
- **batch_conversion.py** - Directory batch processing
- **format_analysis.py** - Binary format analysis

## Common Workflows

### Workflow 1: Converting User Presets

```bash
# 1. Backup original files
cp -r ~/presets/gp5/ ~/presets/gp5_backup/

# 2. Convert to GP-50
gp-convert ~/presets/gp5/ -o ~/presets/gp50/ -v

# 3. Verify conversion
ls -l ~/presets/gp50/
```

### Workflow 2: Analyzing Unknown Presets

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer
from gp_presets_converter.utils import HexDumper

# Analyze structure
analyzer = BinaryAnalyzer()
analysis = analyzer.analyze_file(Path("unknown.preset"))

# Generate hex dump
dumper = HexDumper()
with open("unknown.preset", "rb") as f:
    data = f.read()
    print(dumper.dump(data, max_bytes=512))

# Save analysis results
with open("analysis.txt", "w") as f:
    f.write(f"File Size: {analysis['file_size']}\n")
    f.write(f"Signature: {analysis['signature']}\n")
    f.write(f"Strings: {analysis['possible_strings']}\n")
```

### Workflow 3: Batch Processing with Error Handling

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
input_dir = Path("./gp5_presets/")

successful = []
failed = []

for preset_file in input_dir.glob("*.gp5"):
    try:
        output = converter.convert_file(preset_file)
        successful.append(output)
        print(f"✓ {preset_file.name}")
    except Exception as e:
        failed.append((preset_file, str(e)))
        print(f"✗ {preset_file.name}: {e}")

print(f"\nResults: {len(successful)} succeeded, {len(failed)} failed")
```

## Tips and Best Practices

1. **Always backup original files** before conversion
2. **Test on a few files first** before batch converting
3. **Use verbose mode** to see what's happening
4. **Validate converted files** on your device before deleting originals
5. **Keep original files** until you're sure conversions work correctly

## Next Steps

- Learn about [Preset Format Analysis](preset_format_analysis.md)
- Read the [API Reference](api_reference.md) for detailed documentation
- Check [Troubleshooting](troubleshooting.md) if you encounter issues

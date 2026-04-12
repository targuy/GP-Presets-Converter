# Usage Guide

This guide covers basic and advanced usage of the GP Presets Converter.

## Command-Line Interface

### Basic Commands

**Convert a single file (auto-detects direction):**
```bash
gp-convert 55-TimPierce.prst
```

**Convert with explicit target format:**
```bash
gp-convert preset.prst -t GP50
```

**Convert a directory:**
```bash
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/
```

**Verbose output:**
```bash
gp-convert 55-TimPierce.prst -v
```

**Analyze a preset file:**
```bash
gp-convert preset.prst --analyze
```

**Check version:**
```bash
gp-convert --version
```

**Get help:**
```bash
gp-convert --help
```

### Slot Management (`--slot` / `-s`)

The preset slot number (0–127) is stored in the filename prefix (e.g., `55-TimPierce.prst` → slot 55). Use `--slot N` to set the target slot in the output filename.

**Set target slot for a single file:**
```bash
# Converts 55-TimPierce.prst → 70-TimPierce.prst (in GP-50 format)
gp-convert 55-TimPierce.prst --slot 70
```

**Batch convert with sequential slots starting at 60:**
```bash
# Files are numbered 60-xxx.prst, 61-xxx.prst, 62-xxx.prst, ...
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60
```

### NAM/SnapTone Reference Management (`--nam-offset`)

When a preset references a NAM/SnapTone amp model, the slot reference is embedded in the binary data. If models are loaded into different slots on the source vs target device, use `--nam-offset N` to shift all NAM references.

**Shift NAM references by +5:**
```bash
gp-convert 55-TimPierce.prst --nam-offset 5
```

**Shift NAM references by −3:**
```bash
gp-convert 55-TimPierce.prst --nam-offset -3
```

**Combine slot and NAM offset:**
```bash
gp-convert 55-TimPierce.prst --slot 70 --nam-offset 5
```

> **Note:** When a preset contains a NAM/SnapTone reference and `--nam-offset` is not specified, the converter prints a warning so you can verify the reference is correct.

### Advanced CLI Usage

**Batch conversion with pattern matching:**
```bash
# Convert all .prst files in a directory
gp-convert ./presets/ -o ./converted/
```

**Batch convert with NAM offset and slot assignment:**
```bash
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60 --nam-offset 5
```

## Python API

### Basic Usage

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

# Initialize converter
converter = PresetConverter()

# Convert single file (auto-detects direction)
result = converter.convert_file(Path("55-TimPierce.prst"))
print(f"Converted to: {result}")
```

### Single File with Slot and NAM Offset

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()

# Convert with target slot 70 and NAM offset +5
converter.convert_file(
    Path("55-TimPierce.prst"),
    target_slot=70,
    nam_offset=5,
)
```

### Batch Conversion

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()

# Convert all files with sequential slots starting at 60
converter.convert_directory(
    Path("./GP5_PRESETS/"),
    Path("./GP50_PRESETS/"),
    start_slot=60,
    nam_offset=5,
)
```

### Binary-Level Conversion

```python
from gp_presets_converter.core.converter import CoreConverter

# GP-5 → GP-50
gp50_data = CoreConverter.convert_gp5_to_gp50(gp5_data, nam_offset=5)

# GP-50 → GP-5
gp5_data = CoreConverter.convert_gp50_to_gp5(gp50_data, nam_offset=-5)

# Inspect NAM reference
nam_ref = CoreConverter.get_nam_ref(data)
print(f"NAM slot reference: {nam_ref}")
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
cp -r ~/GP5_PRESETS/ ~/GP5_PRESETS_backup/

# 2. Convert to GP-50 with slot assignment
gp-convert ~/GP5_PRESETS/ -o ~/GP50_PRESETS/ --slot 0 -v

# 3. Verify conversion
ls -l ~/GP50_PRESETS/
```

### Workflow 2: Slot Management

When moving presets between devices you often need to control which slot each preset occupies.

```bash
# Convert and assign to slot 70
gp-convert 55-TimPierce.prst --slot 70
# Output: 70-TimPierce.prst

# Batch — sequential slots starting at 60
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60
# Output: 60-xxx.prst, 61-xxx.prst, 62-xxx.prst, ...
```

### Workflow 3: NAM/SnapTone Reference Management

If your GP-5 and GP-50 have NAM/SnapTone models loaded in different slot positions, the NAM reference inside the preset must be remapped.

**Example:** Your GP-5 presets reference NAM slot 52. On your GP-50 you loaded the same model in slot 57.

```bash
# Shift NAM references by +5 (52 → 57)
gp-convert 55-TimPierce.prst --nam-offset 5
```

Going in the opposite direction:
```bash
# Shift NAM references by −5 (57 → 52)
gp-convert 70-TimPierce.prst --nam-offset -5
```

> A value of 0 in the NAM reference means no NAM model is assigned (built-in amp only). The offset is only applied when the reference is non-zero.

### Workflow 4: Analyzing Unknown Presets

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer
from gp_presets_converter.utils import HexDumper

# Analyze structure
analyzer = BinaryAnalyzer()
analysis = analyzer.analyze_file(Path("unknown.prst"))

# Generate hex dump
dumper = HexDumper()
with open("unknown.prst", "rb") as f:
    data = f.read()
    print(dumper.dump(data, max_bytes=512))

# Save analysis results
with open("analysis.txt", "w") as f:
    f.write(f"File Size: {analysis['file_size']}\n")
    f.write(f"Signature: {analysis['signature']}\n")
    f.write(f"Strings: {analysis['possible_strings']}\n")
```

### Workflow 5: Batch Processing with Error Handling

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
input_dir = Path("./GP5_PRESETS/")

successful = []
failed = []

for preset_file in input_dir.glob("*.prst"):
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

# Conversion Guide

Detailed guide to converting VALETON GP-5 and GP-50 presets bidirectionally.

## Understanding the Conversion Process

Both devices use `.prst` binary files. The converter auto-detects the source format (GP-5: 507 bytes, magic `GP-5\x00`; GP-50: 552 bytes, magic `GP-50`) and converts to the opposite format.

### What Gets Converted

The converter handles:

1. **Binary Header**
   - Magic signature rewritten for the target device
   - Device type tag updated

2. **Effects Chain & Parameters**
   - All effect types, parameters, enable/bypass states, and order
   - Identical effect engine on both devices

3. **Mixer Section**
   - GP-5 has a 2-parameter mixer; GP-50 has 10 parameters
   - Conversion expands or contracts the mixer section accordingly

4. **NAM/SnapTone Reference**
   - Tag `0x0c` value byte at offset `0xA7` (GP-5) / `0xD2` (GP-50)
   - Optionally remapped via `--nam-offset`

5. **Tail Format**
   - Adjusted for the target device's binary layout

### What May Not Convert Perfectly

Some aspects may require adjustment:

1. **Expression Pedal Assignments**
   - GP-50 may have different pedal input configurations
   - May need manual reassignment

2. **NAM/SnapTone Slot References**
   - If NAM models are loaded into different slots on the target device, you must use `--nam-offset` to remap

3. **Device-Specific Features**
   - I/O port configurations differ
   - Some hardware-specific settings

## Conversion Methods

### Method 1: Command-Line (Simplest)

Single file (auto-detects direction):
```bash
gp-convert 55-TimPierce.prst
```

With target slot and NAM offset:
```bash
gp-convert 55-TimPierce.prst --slot 70 --nam-offset 5
```

Entire directory with sequential slots:
```bash
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60
```

### Method 2: Python Script (More Control)

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()

# Single file with error handling
try:
    result = converter.convert_file(
        Path("55-TimPierce.prst"),
        target_slot=70,
        nam_offset=5,
    )
    print(f"Success: {result}")
except Exception as e:
    print(f"Error: {e}")
```

### Method 3: Programmatic with Validation

```python
from pathlib import Path
from gp_presets_converter import PresetConverter, BinaryAnalyzer
from gp_presets_converter.core import PresetParser
from gp_presets_converter.utils import PresetValidator

# Parse original
parser = PresetParser()
preset_data = parser.parse_file(Path("input.gp5"))

# Validate before conversion
validator = PresetValidator()
is_valid, errors = validator.validate_preset_name(preset_data.name)
if not is_valid:
    print(f"Validation errors: {errors}")
    # Fix issues
    preset_data.name = validator.sanitize_preset_name(preset_data.name)

# Convert
converter = PresetConverter()
result = converter.convert_file(Path("input.gp5"), Path("output.gp50"))

# Verify output
analyzer = BinaryAnalyzer()
analysis = analyzer.analyze_file(result)
print(f"Output file size: {analysis['file_size']} bytes")
```

## Step-by-Step Conversion Workflow

### 1. Preparation

**Backup your presets:**
```bash
cp -r ~/gp5_presets ~/gp5_presets_backup
```

**Organize files:**
```
presets/
├── gp5/
│   ├── factory/
│   ├── user/
│   └── community/
└── gp50/  # Will contain converted files
```

### 2. Test Conversion

Convert a few test files first:

```bash
gp-convert 55-TimPierce.prst -v
gp-convert 01-CleanJazz.prst --slot 80 -v
```

### 3. Verify on Device

1. Transfer test files to the target device (GP-50 or GP-5)
2. Load and test each preset
3. Check that all effects work correctly
4. Verify NAM/SnapTone references are correct

### 4. Batch Conversion

Once satisfied with test conversions:

```bash
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 0 -v
```

### 5. Post-Conversion Checks

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Check all converted files
gp50_dir = Path("./GP50_PRESETS/")
for preset in gp50_dir.glob("*.prst"):
    analysis = analyzer.analyze_file(preset)
    print(f"{preset.name}: {analysis['file_size']} bytes")
```

## Slot Number Management

The preset slot number (0–127) is stored **only in the filename prefix** — it is not embedded in the binary data. The filename format is `NN-PresetName.prst` where `NN` is the slot number.

### Single File

```bash
# Original: 55-TimPierce.prst → Output: 70-TimPierce.prst (as GP-50)
gp-convert 55-TimPierce.prst --slot 70
```

### Batch with Sequential Numbering

```bash
# Files numbered sequentially starting at slot 60
gp-convert ./GP5_PRESETS/ -o ./GP50_PRESETS/ --slot 60
# 60-xxx.prst, 61-xxx.prst, 62-xxx.prst, ...
```

### When to Use `--slot`

- **Reorganizing presets** on the target device
- **Avoiding overwrites** when the target slot is already occupied
- **Standardizing slot layout** across devices

## NAM/SnapTone Slot Management

Both the GP-5 and GP-50 support VALETON's NAM/SnapTone amp models. These models are loaded into numbered user slots on each device independently.

### How NAM References Work

- The NAM slot reference is a single byte stored at offset `0xA7` (GP-5) or `0xD2` (GP-50) with tag `0x0c`.
- Value `0` = no NAM assigned (built-in amp only).
- Both devices use the same numbering scheme (e.g., 50–59 in typical setups).

### When to Use `--nam-offset`

Use `--nam-offset` when your NAM models are loaded in **different slot positions** on the source and target device.

**Example:** GP-5 preset references NAM slot 52. On your GP-50, that model sits in slot 57.

```bash
gp-convert 55-TimPierce.prst --nam-offset 5
# NAM ref 52 → 57
```

**Reverse direction:**
```bash
gp-convert 70-TimPierce.prst --nam-offset -5
# NAM ref 57 → 52
```

### NAM Warning

If a preset references a NAM/SnapTone slot and you do **not** specify `--nam-offset`, the converter prints a warning:

```
⚠ Preset references NAM/SnapTone slot 52. Use --nam-offset if slots differ on target device.
```

This is informational only — the conversion still proceeds. If your devices use the same NAM slot layout, you can safely ignore the warning.

## Troubleshooting Conversions

### Issue: Conversion Fails

**Check file integrity:**
```python
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
try:
    analysis = analyzer.analyze_file("problem_file.gp5")
    print(f"File appears valid: {analysis['file_size']} bytes")
except Exception as e:
    print(f"File may be corrupted: {e}")
```

**Verify format:**
```python
from gp_presets_converter.core import PresetParser

parser = PresetParser()
preset = parser.parse_file("problem_file.gp5")
print(f"Detected format: {preset.format}")
```

### Issue: Preset Doesn't Sound Right on GP-50

1. **Check effect parameters:**
   - Some parameters may have different ranges
   - Effects may be in different order

2. **Verify expression pedal:**
   - Pedal assignments may differ
   - Reassign in GP-50 settings

3. **Compare with original:**
   - Load original on GP-5
   - Load converted on GP-50
   - Adjust discrepancies manually

### Issue: Preset Name Incorrect

```python
from gp_presets_converter.utils import PresetValidator

# Validate and fix name
validator = PresetValidator()
name = "My/Invalid:Name*"
is_valid, error = validator.validate_preset_name(name)

if not is_valid:
    clean_name = validator.sanitize_preset_name(name)
    print(f"Fixed name: {clean_name}")
```

## Advanced Conversion Options

### Custom Parameter Mapping

When you need custom conversion rules:

```python
from gp_presets_converter.core import CoreConverter
from gp_presets_converter.models import GP5Preset

# Create custom converter
converter = CoreConverter()

# Load and modify conversion rules
converter.conversion_rules["parameter_mapping"]["custom_param"] = "gp50_param"

# Convert with custom rules
gp5_preset = GP5Preset(name="Test", version="1.0", parameters={})
gp50_preset = converter.convert(gp5_preset)
```

### Batch Conversion with Filters

Convert only specific types:

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
input_dir = Path("gp5/")

# Convert only files matching pattern
for preset in input_dir.glob("blues_*.gp5"):
    output = Path(f"gp50/{preset.stem}.gp50")
    converter.convert_file(preset, output)
```

### Conversion with Validation

```python
from pathlib import Path
from gp_presets_converter import PresetConverter
from gp_presets_converter.core import CoreConverter, PresetParser
from gp_presets_converter.models import GP5Preset

# Parse original
parser = PresetParser()
data = parser.parse_file(Path("input.gp5"))

# Convert to GP5Preset model
gp5_preset = GP5Preset(
    name=data.name,
    version=data.version,
    parameters=data.parameters
)

# Check compatibility
core_converter = CoreConverter()
is_compatible, warnings = core_converter.check_compatibility(gp5_preset)

if not is_compatible:
    print("Warnings:")
    for warning in warnings:
        print(f"  - {warning}")

# Convert anyway
gp50_preset = core_converter.convert(gp5_preset)
```

## Best Practices

1. **Always backup** original presets before converting
2. **Test thoroughly** on your GP-50 device
3. **Keep originals** until you're certain conversions work
4. **Document changes** if you modify converted presets
5. **Share findings** with the community to improve the converter

## Next Steps

- Learn about [Preset Format Analysis](preset_format_analysis.md)
- Check [Troubleshooting Guide](troubleshooting.md) for common issues
- Review [API Reference](api_reference.md) for advanced usage

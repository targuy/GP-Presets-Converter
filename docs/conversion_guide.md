# Conversion Guide

Detailed guide to converting VALETON GP-5 presets to GP-50 format.

## Understanding the Conversion Process

### What Gets Converted

The converter handles:

1. **Preset Metadata**
   - Preset name
   - Version information
   - Creation date (if present)

2. **Global Parameters**
   - Input gain
   - Output level
   - Noise gate settings

3. **Effects Chain**
   - Effect types
   - Effect parameters
   - Enable/bypass states
   - Effect order

4. **Signal Routing**
   - Effect connections
   - Parallel/serial configuration

### What May Not Convert Perfectly

Some aspects may require adjustment:

1. **Expression Pedal Assignments**
   - GP-50 may have different pedal input configurations
   - May need manual reassignment

2. **Device-Specific Features**
   - I/O port configurations differ
   - Some hardware-specific settings

3. **Effect Availability**
   - Rare: Some effects may be model-specific
   - Usually: Both devices share the same effect engine

## Conversion Methods

### Method 1: Command-Line (Simplest)

Single file:
```bash
gp-convert my_preset.gp5 -o my_preset.gp50
```

Entire directory:
```bash
gp-convert ./gp5_presets/ -o ./gp50_presets/ -v
```

### Method 2: Python Script (More Control)

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()

# Single file with error handling
try:
    result = converter.convert_file(
        Path("input.gp5"),
        Path("output.gp50")
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
gp-convert presets/gp5/user/test1.gp5 -o presets/gp50/test1.gp50 -v
gp-convert presets/gp5/user/test2.gp5 -o presets/gp50/test2.gp50 -v
```

### 3. Verify on Device

1. Transfer test files to GP-50
2. Load and test each preset
3. Check that all effects work correctly
4. Verify parameter values

### 4. Batch Conversion

Once satisfied with test conversions:

```bash
gp-convert presets/gp5/user/ -o presets/gp50/user/ -v
```

### 5. Post-Conversion Checks

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Check all converted files
gp50_dir = Path("presets/gp50/user/")
for preset in gp50_dir.glob("*.gp50"):
    analysis = analyzer.analyze_file(preset)
    print(f"{preset.name}: {analysis['file_size']} bytes")
```

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

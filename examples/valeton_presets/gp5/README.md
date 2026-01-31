# GP-5 Preset Files

This directory contains VALETON GP-5 preset files.

## About the GP-5

The VALETON GP-5 is a multi-effects guitar pedal featuring:
- Amp simulation
- Multiple effect types (overdrive, delay, reverb, modulation, etc.)
- Expression pedal input
- MIDI capabilities
- USB connectivity

## File Format

GP-5 preset files are binary files that contain:
- Preset name and metadata
- Effect chain configuration
- Parameter values for each effect
- Routing and signal flow information
- MIDI and expression pedal assignments

The exact binary format is proprietary and being reverse-engineered through analysis.

## Subdirectories

- **factory/** - Factory/stock presets that come with the GP-5
- **user/** - User-created custom presets
- **community/** - Community-contributed presets from other GP-5 users

## Format Analysis

To analyze GP-5 preset files and understand their structure:

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

# Analyze a GP-5 preset file
analyzer = BinaryAnalyzer()
analysis = analyzer.analyze_file(Path("factory/preset_name.gp5"))

print(f"File signature: {analysis['signature']}")
print(f"Detected strings: {analysis['possible_strings']}")
print(f"Structure hints: {analysis['structure_hints']}")
```

## Converting to GP-50

To convert GP-5 presets to GP-50 format:

```python
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()
converter.convert_file(
    Path("gp5/factory/preset_name.gp5"),
    Path("gp50/factory/preset_name.gp50")
)
```

## Notes

- GP-5 and GP-50 share the same internal engine
- The main differences are in I/O configuration and user interface
- Most GP-5 presets should convert cleanly to GP-50 format
- Some features may not map perfectly between formats

# VALETON Preset Format Analysis Notes

This document contains detailed notes on the binary structure of VALETON GP-5 and GP-50 preset files.

## Current Status

🚧 **WORK IN PROGRESS** 🚧

The VALETON preset file formats are proprietary and not publicly documented. This document represents ongoing reverse-engineering efforts to understand their structure.

## File Signatures

### GP-5 Format
- **Suspected Signature**: To be determined through analysis
- **File Extension**: `.gp5` or `.preset`
- **Typical Size Range**: TBD bytes

### GP-50 Format
- **Suspected Signature**: To be determined through analysis
- **File Extension**: `.gp50` or `.preset`
- **Typical Size Range**: TBD bytes

## Preliminary Structure Analysis

### Common Structure Elements (Hypothesis)

Most binary preset formats follow a similar pattern:

```
[HEADER]
  - Magic number / signature (4-8 bytes)
  - Format version (2-4 bytes)
  - Header size (2-4 bytes)
  
[METADATA]
  - Preset name (fixed length string, typically 16-64 bytes)
  - Author/creator info (optional)
  - Timestamp (optional)
  - Tags/categories (optional)

[PARAMETER DATA]
  - Number of effects (1-2 bytes)
  - Effect chain:
    - Effect type ID (1-2 bytes)
    - Effect parameters (variable length)
    - Enable/bypass flags (1 byte)
  
[ROUTING/CONFIGURATION]
  - Signal routing information
  - Input/output configuration
  - Expression pedal assignments
  - MIDI mapping

[FOOTER]
  - Checksum or CRC (2-4 bytes)
  - End marker (optional)
```

## Known Effect Types

Based on GP-5/GP-50 documentation, these effects are available:

### Amplifier Simulation
- Clean amps (various models)
- Crunch/overdrive amps
- High-gain/distortion amps
- Bass amps

### Distortion/Overdrive
- Overdrive
- Distortion
- Fuzz
- Boost

### Modulation
- Chorus
- Flanger
- Phaser
- Tremolo
- Vibrato
- Rotary speaker

### Time-Based
- Delay (various types)
- Reverb (various types)
- Echo

### Dynamics
- Compressor
- Limiter
- Noise gate

### Filter/EQ
- EQ (graphic and parametric)
- Wah
- Auto-wah
- Tone controls

### Other
- Pitch shifter
- Harmonizer
- Octaver

## Parameter Encoding

### Hypothesis

Parameters are likely encoded as:
- **Continuous parameters** (0-100%): Single byte (0-127) or two bytes (0-1023)
- **Toggle parameters** (on/off): Single bit or byte (0/1)
- **Enumerated types** (effect models): Single byte or nibble

## Analysis Methodology

To analyze unknown preset files:

1. **Hex dump comparison**: Compare multiple preset files to identify:
   - Common headers/footers
   - Parameter locations
   - String storage format

2. **Pattern recognition**: Look for:
   - Repeated structures (effect blocks)
   - Null-terminated strings
   - Magic numbers
   - Checksums

3. **Boundary detection**: Identify:
   - Header/body boundaries
   - Effect block boundaries
   - Metadata sections

4. **Statistical analysis**: Examine:
   - Byte value distributions
   - Null byte patterns
   - Common value ranges

## Example Analysis Code

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

# Analyze multiple files to find patterns
analyzer = BinaryAnalyzer()

files = [
    Path("../gp5/factory/preset1.gp5"),
    Path("../gp5/factory/preset2.gp5"),
    Path("../gp5/factory/preset3.gp5"),
]

for file in files:
    print(f"\n=== Analyzing {file.name} ===")
    analysis = analyzer.analyze_file(file)
    
    print(f"Signature: {analysis['signature']}")
    print(f"Size: {analysis['file_size']} bytes")
    print(f"Strings: {analysis['possible_strings'][:5]}")
    print(f"Structure hints: {analysis['structure_hints']}")
```

## Discoveries

### [Date] - [Your Name]
- **Finding**: Description of what was discovered
- **Evidence**: Hex offsets, patterns, or code demonstrating the finding
- **Impact**: How this affects parsing or conversion

### Example Entry
- **Finding**: Preset name appears at offset 0x10
- **Evidence**: 
  ```
  00000010  4D 79 20 50 72 65 73 65  74 00 00 00 00 00 00 00  |My Preset.......|
  ```
- **Impact**: Parser can extract preset name by reading 16 bytes at offset 0x10

## Contributing

To contribute to format analysis:

1. Analyze preset files using the provided tools
2. Document any patterns or structures you discover
3. Include hex dumps and example code
4. Update this document with your findings
5. Submit via pull request

## Resources

- [VALETON Official Website](https://www.valeton-effect.com/)
- [GP-5 Manual](https://www.valeton-effect.com/) (if available)
- [GP-50 Manual](https://www.valeton-effect.com/) (if available)

## Legal Notice

This analysis is performed for interoperability purposes. All analysis is based on publicly available preset files and does not involve disassembly of firmware or proprietary software.

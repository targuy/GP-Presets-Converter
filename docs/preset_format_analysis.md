# Preset Format Analysis

Understanding the binary structure of VALETON GP-5 and GP-50 preset files.

## Overview

This document describes the methodology and findings from analyzing VALETON preset file formats. Since these formats are proprietary and not publicly documented, this represents reverse-engineering efforts.

## Analysis Methodology

### 1. Binary Inspection

Start with basic hex dump analysis:

```python
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
analysis = analyzer.analyze_file("preset.gp5")

print(f"Signature: {analysis['signature']}")
print(f"Structure hints: {analysis['structure_hints']}")
```

### 2. Pattern Recognition

Compare multiple preset files to identify:
- Common headers and footers
- Parameter storage locations
- String encoding methods
- Data structure patterns

### 3. Incremental Changes

Create presets with single parameter changes to isolate:
- Parameter locations in binary data
- Value encoding methods
- Parameter ranges

### 4. Statistical Analysis

Examine byte distributions to detect:
- Null-padded sections
- Compressed data
- Checksum locations

## File Structure Hypothesis

Based on analysis, preset files likely follow this structure:

```
┌─────────────────────────────────────┐
│ HEADER (64-256 bytes)               │
│  - Magic signature (4-8 bytes)      │
│  - Format version (2-4 bytes)       │
│  - Preset metadata                  │
│  - Header size indicator            │
├─────────────────────────────────────┤
│ PRESET NAME (16-64 bytes)           │
│  - Null-terminated or fixed length  │
│  - UTF-8 or ASCII encoding          │
├─────────────────────────────────────┤
│ GLOBAL PARAMETERS (variable)        │
│  - Input gain                       │
│  - Output level                     │
│  - Noise gate settings              │
│  - Expression pedal assignments     │
├─────────────────────────────────────┤
│ EFFECTS CHAIN (variable)            │
│  For each effect:                   │
│  - Effect type ID (1-2 bytes)       │
│  - Enable flag (1 bit)              │
│  - Parameters (variable)            │
│  - Effect-specific data             │
├─────────────────────────────────────┤
│ ROUTING CONFIGURATION (variable)    │
│  - Signal flow                      │
│  - Effect order                     │
│  - Parallel/serial routing          │
├─────────────────────────────────────┤
│ FOOTER (optional, 4-16 bytes)       │
│  - Checksum or CRC                  │
│  - End marker                       │
└─────────────────────────────────────┘
```

## Format Signatures

### GP-5 Format

**Current hypothesis:**
- Signature: To be determined
- Version location: To be determined
- Typical file size: 200-2000 bytes

### GP-50 Format

**Current hypothesis:**
- Signature: To be determined
- Version location: To be determined
- Typical file size: 200-2000 bytes

## Parameter Encoding

### Continuous Parameters

Most continuous parameters (0-100%) are likely encoded as:

- **Single byte (0-127)**: Common for simple parameters
- **Two bytes (0-1023)**: For higher precision
- **Normalized float (0.0-1.0)**: Less common in embedded systems

### Boolean Parameters

On/off switches are typically:
- Single bit in a flags byte
- Full byte (0x00 = off, 0x01 = on)

### Effect Type IDs

Effect types are likely assigned numeric IDs:

```
Hypothetical mapping:
0x01 = Compressor
0x02 = Overdrive
0x03 = Distortion
0x04 = EQ
0x05 = Delay
0x06 = Reverb
... etc
```

## String Encoding

Preset names and other strings are likely:
- Fixed-length fields (16, 32, or 64 bytes)
- Null-terminated within the field
- UTF-8 or ASCII encoding
- Padded with null bytes

## Analysis Tools

### Hex Dump with Annotations

```python
from gp_presets_converter.utils import HexDumper

dumper = HexDumper()
with open("preset.gp5", "rb") as f:
    data = f.read()

annotations = {
    0x00: "File signature",
    0x10: "Preset name",
    0x30: "Parameters section"
}

print(dumper.dump_with_annotations(data, annotations, max_bytes=256))
```

### File Comparison

```python
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
comparison = analyzer.compare_files("preset1.gp5", "preset2.gp5")

print(f"Similarity: {comparison['similarity_percentage']}%")
for diff in comparison['first_differences'][:20]:
    print(f"Offset {diff['offset']:04X}: {diff['file1_value']} → {diff['file2_value']}")
```

### Pattern Detection

```python
from gp_presets_converter.utils import HexDumper

dumper = HexDumper()
with open("preset.gp5", "rb") as f:
    data = f.read()

# Find all occurrences of a pattern
pattern = b"\x00\x00\xFF\xFF"
offsets = dumper.find_patterns(data, pattern)
print(f"Pattern found at offsets: {offsets}")
```

## Conversion Challenges

### Format Differences

GP-5 and GP-50 likely differ in:

1. **I/O Configuration**
   - Different port layouts
   - Expression pedal mappings may differ

2. **Effect Availability**
   - Some effects may be exclusive to one model
   - Effect parameters might have different ranges

3. **Firmware Versions**
   - Format may vary between firmware versions

### Conversion Strategy

1. **Parse source format** → Extract all parameters
2. **Map parameters** → GP-5 params → GP-50 params
3. **Validate ranges** → Ensure values fit GP-50 limits
4. **Serialize** → Write GP-50 binary format

## Checksum Algorithms

Common checksum methods in embedded devices:

### Simple Sum
```python
def calculate_checksum(data: bytes) -> int:
    return sum(data) & 0xFF
```

### CRC16
```python
import crc16
def calculate_crc(data: bytes) -> int:
    return crc16.crc16xmodem(data)
```

### XOR Checksum
```python
def xor_checksum(data: bytes) -> int:
    result = 0
    for byte in data:
        result ^= byte
    return result
```

## Contributing Analysis

When you discover format details:

1. **Document the finding**
   - Offset location
   - Data type and size
   - Value range
   - Encoding method

2. **Provide evidence**
   - Hex dumps showing the pattern
   - Multiple examples
   - Edge cases

3. **Submit updates**
   - Update `examples/valeton_presets/analysis/format_notes.md`
   - Include code demonstrating parsing
   - Add test cases

## Resources

- [Binary File Analysis](https://en.wikipedia.org/wiki/Binary_file)
- [Hex Editors](https://en.wikipedia.org/wiki/Hex_editor)
- [Reverse Engineering Techniques](https://en.wikipedia.org/wiki/Reverse_engineering)

## Legal Considerations

This analysis is performed for interoperability purposes under fair use principles. We do not disassemble firmware or violate any copyright protections.

# Preset Format Analysis

Binary structure of VALETON GP-5 and GP-50 `.prst` preset files — based on reverse-engineering actual firmware presets.

## Overview

Both the GP-5 and GP-50 use `.prst` binary files. The formats share the same internal effect/parameter engine but differ in file size, mixer section width, device type tag, and tail layout.

| Property | GP-5 | GP-50 |
|---|---|---|
| File size | 507 bytes | 552 bytes |
| Magic signature | `GP-5\x00` (5 bytes) | `GP-50` (5 bytes) |
| Mixer params | 2 | 10 |
| NAM/SnapTone offset | `0xA7` | `0xD2` |
| Size difference | — | +45 bytes |

The 45-byte difference comes from: expanded mixer section (2 → 10 parameters), different device type tag, and different tail format.

## Discovered Binary Layout

### GP-5 (507 bytes)

```
Offset   Size    Description
──────   ────    ───────────────────────────────
0x00     5       Magic signature: "GP-5\x00"
0x05     ...     Header / metadata
  ...    ...     Effects chain (tag-value pairs)
0xA7     1       NAM/SnapTone slot reference (tag 0x0c value byte)
  ...    ...     Remaining FX body
  ...    2       Mixer section (2 parameters)
  ...    ...     Tail / footer
──────   ────    ───────────────────────────────
Total    507     bytes
```

### GP-50 (552 bytes)

```
Offset   Size    Description
──────   ────    ───────────────────────────────
0x00     5       Magic signature: "GP-50"
0x05     ...     Header / metadata
  ...    ...     Effects chain (tag-value pairs)
0xD2     1       NAM/SnapTone slot reference (tag 0x0c value byte)
  ...    ...     Remaining FX body
  ...    10      Mixer section (10 parameters)
  ...    ...     Tail / footer
──────   ────    ───────────────────────────────
Total    552     bytes
```

## Key Findings

### Slot Number — Filename Only

The preset slot number (0–127) is **NOT stored inside the binary**. It exists only in the filename prefix:

```
55-TimPierce.prst   →  slot 55
01-CleanJazz.prst   →  slot 1
127-HeavyMetal.prst →  slot 127
```

This means renaming the file is sufficient to change its slot position on the device.

### NAM/SnapTone Reference

Both devices support NAM/SnapTone amp models loaded into numbered user slots. The reference is stored as a tag `0x0c` value byte inside the FX body:

- **GP-5 offset:** `0xA7`
- **GP-50 offset:** `0xD2`
- **Value `0`** = no NAM model assigned (built-in amp only)
- **Non-zero value** = NAM/SnapTone slot number (e.g., 50–59 in typical setups)
- Both devices use the **same numbering scheme**

### IR / Cab Reference

The IR/cab reference is stored as tag `0x0f`. In all analyzed presets, the value is a constant `4`. This appears to represent a cab type rather than a user-configurable IR slot.

### Mixer Section

The mixer section is the primary structural difference between the two formats:

- **GP-5:** 2 mixer parameters
- **GP-50:** 10 mixer parameters (8 additional parameters, default-initialized during conversion)

### Device Type Tag

Each format includes a device type identifier that distinguishes the target hardware. This tag is rewritten during conversion.

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

## File Structure

Both formats share the following high-level layout:

```
┌─────────────────────────────────────┐
│ HEADER (5+ bytes)                   │
│  - Magic signature (5 bytes)        │
│  - Device metadata                  │
├─────────────────────────────────────┤
│ EFFECTS CHAIN (variable)            │
│  Tag-value pairs for each effect:   │
│  - Effect type / enable / params    │
│  - Tag 0x0c = NAM/SnapTone ref     │
│  - Tag 0x0f = IR/cab ref (= 4)     │
├─────────────────────────────────────┤
│ MIXER SECTION                       │
│  GP-5:  2 parameters                │
│  GP-50: 10 parameters               │
├─────────────────────────────────────┤
│ TAIL / FOOTER                       │
│  Device-specific tail format        │
└─────────────────────────────────────┘
```

## Format Signatures

### GP-5 Format

- **Signature:** `GP-5\x00` (5 bytes: `0x47 0x50 0x2D 0x35 0x00`)
- **File size:** 507 bytes (all known presets)
- **NAM offset:** `0xA7`

### GP-50 Format

- **Signature:** `GP-50` (5 bytes: `0x47 0x50 0x2D 0x35 0x30`)
- **File size:** 552 bytes (all known presets)
- **NAM offset:** `0xD2`

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

## Conversion Mapping

The binary conversion between GP-5 and GP-50 involves:

1. **Rewrite magic signature** — `GP-5\x00` ↔ `GP-50`
2. **Expand/contract mixer** — 2 params ↔ 10 params (extra 8 params default-initialized)
3. **Update device type tag**
4. **Adjust tail format**
5. **Optionally remap NAM reference** — apply signed offset to tag `0x0c` value

No checksum has been found in the file format; files appear to be accepted as-is by the devices.

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

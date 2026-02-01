# Preset Format Analysis

This directory contains analysis results and documentation for VALETON preset file formats.

## Contents

- **format_notes.md** - Detailed notes on binary format structure
- **hex_dumps/** - Hex dump files of sample presets for analysis

## Binary Format Analysis

The GP-5 and GP-50 preset formats are proprietary binary formats. This directory contains the results of reverse-engineering efforts to understand their structure.

## Analysis Tools

Use the built-in analysis tools to examine preset files:

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Analyze a single file
analysis = analyzer.analyze_file(Path("../gp5/factory/preset1.gp5"))

print("=== File Analysis ===")
print(f"Size: {analysis['file_size']} bytes")
print(f"Signature: {analysis['signature']}")
print(f"\nDetected strings:")
for s in analysis['possible_strings']:
    print(f"  - {s}")

print(f"\nByte distribution:")
print(f"  Min: {analysis['byte_distribution']['min']}")
print(f"  Max: {analysis['byte_distribution']['max']}")
print(f"  Mean: {analysis['byte_distribution']['mean']:.2f}")
print(f"  Null bytes: {analysis['byte_distribution']['null_percentage']:.1f}%")

print(f"\nHex preview:")
print(analysis['hex_preview'])
```

## Comparing Files

Compare two preset files to identify differences:

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()

# Compare two similar presets
comparison = analyzer.compare_files(
    Path("../gp5/factory/preset1.gp5"),
    Path("../gp5/factory/preset2.gp5")
)

print(f"File 1 size: {comparison['file1_size']} bytes")
print(f"File 2 size: {comparison['file2_size']} bytes")
print(f"Byte differences: {comparison['byte_differences']}")
print(f"Similarity: {comparison['similarity_percentage']:.1f}%")

print(f"\nFirst differences:")
for diff in comparison['first_differences'][:10]:
    print(f"  Offset {diff['offset']:04X}: {diff['file1_value']} -> {diff['file2_value']}")
```

## Format Documentation

See `format_notes.md` for detailed documentation about:
- File header structure
- Parameter encoding
- Effect data layout
- Checksum algorithms
- Known signatures and magic numbers

## Contributing Analysis

If you discover new information about the preset formats:

1. Document your findings in `format_notes.md`
2. Include hex dumps demonstrating the discovery
3. Provide sample code showing how to parse the structure
4. Submit via pull request

Your contributions help everyone understand and work with these formats!

## Hex Dumps

The `hex_dumps/` directory contains annotated hex dumps of sample preset files. These are useful references for understanding the binary structure.

To generate a hex dump:

```python
from pathlib import Path
from gp_presets_converter.utils import HexDumper, FileHandler

# Read preset file
data = FileHandler.read_binary(Path("../gp5/factory/preset1.gp5"))

# Generate hex dump
dumper = HexDumper()
hex_output = dumper.dump(data, max_bytes=1024)

# Save to file
with open("hex_dumps/preset1_analysis.txt", "w") as f:
    f.write(hex_output)

print("Hex dump saved to hex_dumps/preset1_analysis.txt")
```

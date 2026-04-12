# API Reference

Complete API documentation for the GP Presets Converter package.

## Main Classes

### PresetConverter

Main class for converting preset files between GP-5 and GP-50 formats.

```python
from gp_presets_converter import PresetConverter

converter = PresetConverter()
```

#### Methods

**`convert_file(input_path: Path, output_path: Optional[Path] = None, *, target_slot: Optional[int] = None, nam_offset: int = 0) -> Path`**

Convert a single `.prst` preset file. Auto-detects GP-5 vs GP-50 and converts to the opposite format.

- **Parameters:**
  - `input_path`: Path to the input `.prst` preset file
  - `output_path`: Optional output path (auto-generated if not provided)
  - `target_slot`: Optional slot number (0–127) for the output filename
  - `nam_offset`: Signed integer offset to remap NAM/SnapTone slot references (default `0`)
- **Returns:** Path to the converted file
- **Raises:** `FileNotFoundError`, `ValueError`

**`convert_directory(input_dir: Path, output_dir: Optional[Path] = None, *, start_slot: Optional[int] = None, nam_offset: int = 0) -> list[Path]`**

Convert all `.prst` files in a directory.

- **Parameters:**
  - `input_dir`: Directory containing preset files
  - `output_dir`: Optional output directory
  - `start_slot`: Optional starting slot number; files are numbered sequentially from this value
  - `nam_offset`: Signed integer offset to remap NAM/SnapTone slot references (default `0`)
- **Returns:** List of converted file paths
- **Raises:** `NotADirectoryError`

---

### BinaryAnalyzer

Tools for analyzing binary preset files.

```python
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
```

#### Methods

**`analyze_file(file_path: Path) -> Dict[str, Any]`**

Perform comprehensive analysis of a binary file.

- **Parameters:** `file_path` - Path to file to analyze
- **Returns:** Dictionary with analysis results
- **Raises:** `FileNotFoundError`

**`compare_files(file1: Path, file2: Path) -> Dict[str, Any]`**

Compare two preset files to identify differences.

- **Parameters:**
  - `file1`: First file to compare
  - `file2`: Second file to compare
- **Returns:** Dictionary with comparison results

---

## Core Modules

### PresetParser

Parser for binary preset files.

```python
from gp_presets_converter.core import PresetParser

parser = PresetParser()
```

#### Methods

**`parse_file(file_path: Path) -> PresetData`**

Parse a preset file and extract data.

- **Parameters:** `file_path` - Path to preset file
- **Returns:** `PresetData` object
- **Raises:** `FileNotFoundError`, `ValueError`

**`validate_checksum(data: bytes) -> bool`**

Validate preset file checksum.

---

### CoreConverter

Core binary conversion logic between GP-5 and GP-50 formats.

```python
from gp_presets_converter.core.converter import CoreConverter
```

#### Static / Class Methods

**`convert_gp5_to_gp50(data: bytes, nam_offset: int = 0) -> bytes`**

Convert raw GP-5 binary data (507 bytes) to GP-50 format (552 bytes).

- **Parameters:**
  - `data`: Raw GP-5 binary data
  - `nam_offset`: Signed integer offset applied to NAM/SnapTone slot reference (default `0`)
- **Returns:** Raw GP-50 binary data
- **Raises:** `ValueError`

**`convert_gp50_to_gp5(data: bytes, nam_offset: int = 0) -> bytes`**

Convert raw GP-50 binary data (552 bytes) to GP-5 format (507 bytes).

- **Parameters:**
  - `data`: Raw GP-50 binary data
  - `nam_offset`: Signed integer offset applied to NAM/SnapTone slot reference (default `0`)
- **Returns:** Raw GP-5 binary data
- **Raises:** `ValueError`

**`get_nam_ref(data: bytes) -> int`**

Read the NAM/SnapTone slot reference from raw preset data. Returns the tag `0x0c` value byte.

- **Parameters:** `data` — Raw GP-5 or GP-50 binary data
- **Returns:** NAM slot number (`0` = no NAM assigned)

**`remap_nam_ref(data: bytes, offset: int) -> bytes`**

Return a copy of the preset data with the NAM/SnapTone slot reference shifted by `offset`. Only applied when the current reference is non-zero.

- **Parameters:**
  - `data`: Raw preset binary data
  - `offset`: Signed integer offset
- **Returns:** Modified binary data

**`convert(gp5_preset: GP5Preset) -> GP50Preset`**

Convert GP-5 preset model to GP-50 preset model.

- **Parameters:** `gp5_preset` - GP5Preset object
- **Returns:** GP50Preset object
- **Raises:** `ValueError`

**`check_compatibility(gp5_preset: GP5Preset) -> tuple[bool, list[str]]`**

Check if preset can be fully converted.

- **Returns:** Tuple of (is_compatible, warnings_list)

---

### PresetWriter

Writer for preset files.

```python
from gp_presets_converter.core import PresetWriter

writer = PresetWriter()
```

#### Methods

**`write_gp50(preset: GP50Preset, output_path: Path) -> None`**

Write GP-50 preset to disk.

- **Parameters:**
  - `preset`: GP50Preset object to write
  - `output_path`: Output file path
- **Raises:** `IOError`

**`create_backup(file_path: Path) -> Optional[Path]`**

Create backup of existing file.

- **Returns:** Path to backup file or None

---

## Data Models

### GP5Preset

Data model for GP-5 presets.

```python
from gp_presets_converter.models import GP5Preset

preset = GP5Preset(
    name="My Preset",
    version="1.0",
    parameters={"input_gain": 50}
)
```

#### Methods

- `to_dict() -> Dict[str, Any]`
- `from_dict(data: Dict[str, Any]) -> None`
- `validate() -> tuple[bool, List[str]]`
- `add_effect(effect: Dict[str, Any]) -> None`
- `remove_effect(index: int) -> None`

---

### GP50Preset

Data model for GP-50 presets.

```python
from gp_presets_converter.models import GP50Preset

preset = GP50Preset(
    name="My GP50 Preset",
    version="1.0",
    parameters={"input_gain": 50}
)
```

#### Methods

- `to_dict() -> Dict[str, Any]`
- `from_dict(data: Dict[str, Any]) -> None`
- `validate() -> tuple[bool, List[str]]`
- `add_effect(effect: Dict[str, Any]) -> None`
- `set_expression_pedal(parameter: str) -> None`

---

### PresetData

Generic preset data container.

```python
from gp_presets_converter.models import PresetData

data = PresetData(
    format="GP5",
    version="1.0",
    name="Preset Name",
    parameters={},
    raw_data=b"..."
)
```

---

## Utility Functions

### Slot Filename Helpers

```python
from gp_presets_converter.utils import file_handler
```

**`_parse_slot_from_filename(filename: str) -> Optional[int]`**

Extract the slot number from a preset filename prefix.

- **Parameters:** `filename` — e.g., `"55-TimPierce.prst"`
- **Returns:** Slot number as `int` (e.g., `55`), or `None` if no prefix found

**`_replace_slot_in_filename(filename: str, new_slot: int) -> str`**

Return a new filename with the slot prefix replaced.

- **Parameters:**
  - `filename`: Original filename (e.g., `"55-TimPierce.prst"`)
  - `new_slot`: New slot number (0–127)
- **Returns:** Updated filename (e.g., `"70-TimPierce.prst"`)

---

## Utility Classes

### FileHandler

Utilities for file operations.

```python
from gp_presets_converter.utils import FileHandler
```

#### Static Methods

- `read_binary(file_path: Path) -> bytes`
- `write_binary(file_path: Path, data: bytes, create_backup: bool = True) -> None`
- `create_backup(file_path: Path) -> Path`
- `find_preset_files(directory: Path, extensions: Optional[List[str]] = None) -> List[Path]`
- `ensure_directory(directory: Path) -> None`

---

### HexDumper

Hex dump utilities for analysis.

```python
from gp_presets_converter.utils import HexDumper

dumper = HexDumper(bytes_per_line=16)
```

#### Methods

- `dump(data: bytes, offset: int = 0, max_bytes: Optional[int] = None) -> str`
- `dump_comparison(data1: bytes, data2: bytes, max_bytes: Optional[int] = None) -> str`
- `dump_with_annotations(data: bytes, annotations: dict[int, str], max_bytes: Optional[int] = None) -> str`
- `find_patterns(data: bytes, pattern: bytes) -> list[int]`

---

### BinaryReader

Binary data reader with multiple encoding support.

```python
from gp_presets_converter.utils import BinaryReader

reader = BinaryReader(data)
```

#### Methods

- `read_bytes(count: int) -> bytes`
- `read_byte() -> int`
- `read_uint16(little_endian: bool = True) -> int`
- `read_uint32(little_endian: bool = True) -> int`
- `read_string(length: int, encoding: str = "utf-8") -> str`
- `skip(count: int) -> None`
- `seek(offset: int) -> None`

---

### BinaryWriter

Binary data writer.

```python
from gp_presets_converter.utils import BinaryWriter

writer = BinaryWriter()
```

#### Methods

- `write_bytes(data: bytes) -> None`
- `write_byte(value: int) -> None`
- `write_uint16(value: int, little_endian: bool = True) -> None`
- `write_uint32(value: int, little_endian: bool = True) -> None`
- `write_string(text: str, length: int, encoding: str = "utf-8", padding: int = 0) -> None`
- `get_bytes() -> bytes`

---

### PresetValidator

Validation utilities for presets.

```python
from gp_presets_converter.utils import PresetValidator
```

#### Static Methods

- `validate_preset(preset: BasePreset) -> Tuple[bool, List[str]]`
- `validate_parameter_range(name: str, value: Any) -> Tuple[bool, str]`
- `validate_effect(effect: Dict[str, Any]) -> Tuple[bool, List[str]]`
- `validate_preset_name(name: str) -> Tuple[bool, str]`
- `sanitize_preset_name(name: str) -> str`

---

## Configuration

### Settings

Configuration settings for the converter.

```python
from gp_presets_converter.config import Settings

settings = Settings.default()
# or
settings = Settings.for_analysis()
# or
settings = Settings.for_batch_conversion()
```

#### Attributes

- `GP5_EXTENSIONS: List[str]`
- `GP50_EXTENSIONS: List[str]`
- `MIN_PRESET_SIZE: int`
- `MAX_PRESET_SIZE: int`
- `CREATE_BACKUP: bool`
- `VERBOSE: bool`
- `DEBUG: bool`

---

## Type Definitions

Common types used throughout the package:

```python
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path

# Parameter dictionary
Parameters = Dict[str, Any]

# Effect dictionary
Effect = Dict[str, Any]

# Validation result
ValidationResult = Tuple[bool, List[str]]
```

## Examples

See the [Usage Guide](usage.md) for practical examples of using these APIs.

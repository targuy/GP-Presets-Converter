# VALETON Preset Files Collection

This directory contains VALETON GP-5 and GP-50 preset files organized by source and type.

## Directory Structure

- **gp5/** - GP-5 preset files
  - **factory/** - Factory presets included with the GP-5
  - **user/** - User-created presets
  - **community/** - Community-contributed presets
- **gp50/** - GP-50 preset files
  - **factory/** - Factory presets included with the GP-50
  - **user/** - User-created presets
  - **community/** - Community-contributed presets
- **analysis/** - Analysis results and documentation
  - **format_notes.md** - Detailed notes on preset file formats
  - **hex_dumps/** - Hex dump analysis files

## Adding Preset Files

### GP-5 Presets

Place GP-5 preset files (typically with `.gp5` or `.preset` extension) in the appropriate subdirectory:

```
valeton_presets/gp5/
├── factory/        # Stock/factory presets
├── user/          # Your personal presets
└── community/     # Presets from other users
```

### GP-50 Presets

Place GP-50 preset files (typically with `.gp50` or `.preset` extension) in the appropriate subdirectory:

```
valeton_presets/gp50/
├── factory/       # Stock/factory presets
├── user/          # Your personal presets
└── community/     # Presets from other users
```

## Naming Convention

When adding preset files, use descriptive names:

- Good: `blues_crunch_od.gp5`, `ambient_reverb_delay.gp5`
- Avoid: `preset1.gp5`, `untitled.gp5`

Include metadata if possible (artist, song, style).

## File Format Notes

Both GP-5 and GP-50 use binary preset formats. See `analysis/format_notes.md` for detailed information about the file structure and binary layout.

## Analyzing Presets

To analyze the binary structure of a preset file:

```python
from pathlib import Path
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
result = analyzer.analyze_file(Path("valeton_presets/gp5/factory/preset1.gp5"))

# View hex dump
print(result["hex_preview"])

# View detected strings
print(result["possible_strings"])

# View structure hints
print(result["structure_hints"])
```

## Contributing

When contributing preset files:

1. Ensure you have the rights to share them
2. Test them to ensure they work correctly
3. Provide a brief description of the preset's sound/purpose
4. Include any relevant metadata (genre, artist, etc.)
5. Submit via pull request

## Legal

Only contribute preset files that you own or have permission to share. Factory presets should only be included with proper authorization from VALETON.

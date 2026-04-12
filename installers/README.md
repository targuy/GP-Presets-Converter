# Installer Build Scripts

Build standalone executables for GP Presets Converter that don't require Python to be installed.

## Prerequisites

Install the build dependencies:

```bash
pip install pyinstaller
```

## Building

### Windows

```cmd
cd installers
build_windows.bat
```

Output: `dist/gp-convert.exe`

### macOS

```bash
cd installers
chmod +x build_macos.sh
./build_macos.sh
```

Output: `dist/gp-convert` (standalone binary)

### Linux

```bash
cd installers
chmod +x build_linux.sh
./build_linux.sh
```

Output: `dist/gp-convert` (standalone binary)

### All Platforms (Python script)

You can also use the cross-platform build script:

```bash
python installers/build.py
```

This auto-detects your OS and builds the appropriate installer.

## Distribution

After building, the standalone executable is in the `dist/` directory. You can distribute this single file — no Python installation is needed on the target machine.

### Windows

Copy `dist/gp-convert.exe` to any directory in your PATH, or use it directly:

```cmd
gp-convert.exe 55-TimPierce.prst --slot 70
```

### macOS

Copy `dist/gp-convert` to `/usr/local/bin/` or any directory in your PATH:

```bash
cp dist/gp-convert /usr/local/bin/
gp-convert 55-TimPierce.prst --slot 70
```

### Linux

Copy `dist/gp-convert` to `/usr/local/bin/` or `~/.local/bin/`:

```bash
cp dist/gp-convert ~/.local/bin/
gp-convert 55-TimPierce.prst --slot 70
```

## Installer Contents

The standalone executable bundles:

- Python runtime
- GP Presets Converter package
- All dependencies

File sizes are typically:

- **Windows**: ~15-25 MB
- **macOS**: ~15-25 MB
- **Linux**: ~15-25 MB

## Troubleshooting

### "Permission denied" on macOS/Linux

```bash
chmod +x dist/gp-convert
```

### macOS Gatekeeper blocks the app

```bash
xattr -d com.apple.quarantine dist/gp-convert
```

### Antivirus false positive on Windows

PyInstaller executables are sometimes flagged by antivirus software. This is a known false positive. You can add an exception for `gp-convert.exe` in your antivirus settings.

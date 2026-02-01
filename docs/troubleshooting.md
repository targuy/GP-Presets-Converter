# Troubleshooting Guide

Solutions to common issues when using the GP Presets Converter.

## Installation Issues

### "Python version not supported"

**Problem:** Error about Python version < 3.12

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.12
# On Ubuntu/Debian:
sudo apt-get install python3.12

# On macOS with Homebrew:
brew install python@3.12

# Then use python3.12 explicitly
python3.12 -m venv venv
```

### "No module named 'gp_presets_converter'"

**Problem:** Package not found after installation

**Solution:**
```bash
# Reinstall in development mode
pip install -e .

# Or check if virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Verify installation
pip list | grep gp-presets-converter
```

### Permission Errors

**Problem:** Permission denied during installation

**Solution:**
```bash
# Use virtual environment (recommended)
python3.12 -m venv venv
source venv/bin/activate
pip install -e .

# Or install for user only
pip install --user -e .
```

## Conversion Issues

### "FileNotFoundError: Input file not found"

**Problem:** Cannot find input preset file

**Solution:**
```bash
# Check file exists
ls -l path/to/preset.gp5

# Use absolute path
gp-convert /absolute/path/to/preset.gp5 -o output.gp50

# Or ensure working directory is correct
cd /path/to/presets
gp-convert preset.gp5 -o preset.gp50
```

### "Invalid file format"

**Problem:** File is not a valid preset file

**Solution:**
```python
from gp_presets_converter import BinaryAnalyzer

# Analyze file to check format
analyzer = BinaryAnalyzer()
analysis = analyzer.analyze_file("suspicious_file.gp5")

print(f"File size: {analysis['file_size']}")
print(f"Signature: {analysis['signature']}")
print(f"Detected strings: {analysis['possible_strings']}")

# If file is corrupted or wrong format:
# - Check file extension
# - Verify file isn't empty
# - Try re-downloading/re-exporting from device
```

### Conversion Completes But Preset Doesn't Work

**Problem:** Converted file exists but doesn't work on GP-50

**Solution:**

1. **Verify file size is reasonable:**
```python
from pathlib import Path
from gp_presets_converter.utils import FileHandler

size = FileHandler.get_file_size(Path("output.gp50"))
print(f"Output file size: {size} bytes")

# GP-50 presets are typically 200-2000 bytes
if size < 100 or size > 10000:
    print("Warning: Unusual file size")
```

2. **Compare with working preset:**
```python
from gp_presets_converter import BinaryAnalyzer

analyzer = BinaryAnalyzer()
comparison = analyzer.compare_files(
    "working_preset.gp50",
    "converted_preset.gp50"
)

print(f"Similarity: {comparison['similarity_percentage']}%")
```

3. **Check for format-specific issues:**
   - Expression pedal assignments may need adjustment
   - Effect order might differ
   - Some parameters might be out of range

### "NotADirectoryError" During Batch Conversion

**Problem:** Path is a file, not a directory

**Solution:**
```bash
# Check if path is a directory
ls -ld path/to/presets

# If it's a file, use single file conversion
gp-convert path/to/preset.gp5 -o output.gp50

# If it's a directory, ensure path is correct
gp-convert path/to/presets/ -o path/to/output/ -v
```

## Runtime Issues

### "Memory Error" with Large Files

**Problem:** Out of memory when processing large files

**Solution:**
```python
# Process files one at a time
from pathlib import Path
from gp_presets_converter import PresetConverter

converter = PresetConverter()

for preset_file in Path("large_collection").glob("*.gp5"):
    try:
        converter.convert_file(preset_file)
        print(f"✓ {preset_file.name}")
    except MemoryError:
        print(f"✗ {preset_file.name}: File too large")
    except Exception as e:
        print(f"✗ {preset_file.name}: {e}")
```

### Slow Performance

**Problem:** Conversion takes too long

**Solution:**

1. **Use batch processing:**
```python
# Instead of calling CLI repeatedly
for file in *.gp5; do gp-convert $file; done

# Use directory conversion
gp-convert ./presets/ -o ./output/ -v
```

2. **Check file sizes:**
```bash
# Find unusually large files
find . -name "*.gp5" -size +10M
```

3. **Disable verbose output:**
```bash
# Faster without -v flag
gp-convert input_dir/ -o output_dir/
```

### Unicode/Encoding Errors

**Problem:** Error with non-ASCII characters in preset names

**Solution:**
```python
from gp_presets_converter.utils import PresetValidator

# Sanitize preset name
validator = PresetValidator()
name = "Préset ñame with spëcial chars"
clean_name = validator.sanitize_preset_name(name)
print(f"Sanitized: {clean_name}")
```

## Development Issues

### Tests Failing

**Problem:** pytest tests fail

**Solution:**
```bash
# Ensure dev dependencies installed
pip install -e '.[dev]'

# Run tests with verbose output
pytest tests/ -v

# Run specific failing test
pytest tests/test_converter.py::TestClass::test_method -v

# Check for missing dependencies
pip check
```

### Type Checking Errors

**Problem:** mypy reports type errors

**Solution:**
```bash
# Run mypy
mypy src/gp_presets_converter

# If you need to add type: ignore
# result: Dict[str, Any] = func()  # type: ignore[annotation-issue]

# Or update type hints
def func() -> Dict[str, Any]:
    return {}
```

### Import Errors in Development

**Problem:** Cannot import modules during development

**Solution:**
```bash
# Reinstall in editable mode
pip uninstall gp-presets-converter
pip install -e .

# Check PYTHONPATH
echo $PYTHONPATH

# Add project to path if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

## CLI Issues

### "Command not found: gp-convert"

**Problem:** CLI command not available

**Solution:**
```bash
# Check if package installed
pip list | grep gp-presets-converter

# Reinstall
pip install -e .

# Use Python module directly as alternative
python -m gp_presets_converter.cli input.gp5 -o output.gp50

# Check if scripts directory in PATH
which gp-convert

# Add to PATH if needed
export PATH="$PATH:~/.local/bin"  # Linux
# or
export PATH="$PATH:~/Library/Python/3.12/bin"  # macOS
```

### Arguments Not Working

**Problem:** CLI arguments not being recognized

**Solution:**
```bash
# Check argument syntax
gp-convert --help

# Ensure proper spacing and dashes
gp-convert input.gp5 -o output.gp50  # Correct
gp-convert input.gp5 --o output.gp50  # Wrong (single dash for -o)

# Quote paths with spaces
gp-convert "My Presets/preset.gp5" -o "output.gp50"
```

## Platform-Specific Issues

### Windows

**Path separators:**
```python
# Use pathlib for cross-platform compatibility
from pathlib import Path
input_path = Path("presets") / "file.gp5"  # Works on all platforms
```

**Command not found:**
```cmd
# Use py launcher
py -m gp_presets_converter.cli input.gp5 -o output.gp50
```

### macOS

**Certificate errors:**
```bash
# If you get SSL certificate errors
pip install --upgrade certifi
# Or
/Applications/Python\ 3.12/Install\ Certificates.command
```

### Linux

**Permission issues:**
```bash
# Make scripts executable
chmod +x examples/usage_examples/*.py

# Use virtual environment to avoid sudo
python3.12 -m venv venv
source venv/bin/activate
pip install -e '.[dev]'
```

## Getting More Help

### Enable Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

from gp_presets_converter import PresetConverter
converter = PresetConverter()
# Now see detailed debug output
```

### Check System Information

```bash
# Python version
python --version

# Installed packages
pip list

# Package information
pip show gp-presets-converter

# System information
uname -a  # Linux/macOS
systeminfo  # Windows
```

### Report an Issue

When reporting issues on GitHub, include:

1. **Environment details:**
   - OS and version
   - Python version
   - Package version

2. **Steps to reproduce:**
   - Exact commands run
   - Input file characteristics
   - Expected vs actual behavior

3. **Error messages:**
   - Full error traceback
   - Any relevant log output

4. **Minimal example:**
   - Simplest code that reproduces issue
   - Sample input file (if possible)

### Example Issue Report

```
**Environment:**
- OS: Ubuntu 22.04
- Python: 3.12.0
- Package: gp-presets-converter 0.1.0

**Problem:**
Conversion fails with FileNotFoundError

**Steps to reproduce:**
1. Run: gp-convert test.gp5 -o test.gp50
2. Error occurs

**Error message:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'test.gp5'
```

**Additional context:**
File exists and is readable. Using bash on Ubuntu 22.04.
```

## Additional Resources

- [GitHub Issues](https://github.com/targuy/GP-Presets-Converter/issues)
- [Development Guide](development.md)
- [API Reference](api_reference.md)
- [Usage Guide](usage.md)

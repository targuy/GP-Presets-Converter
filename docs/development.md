# Development Guide

Guide for contributing to and developing the GP Presets Converter.

## Setting Up Development Environment

### Prerequisites

- Python 3.12 or higher
- Git
- Code editor (VSCode recommended)

### Initial Setup

1. **Fork and clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/GP-Presets-Converter.git
cd GP-Presets-Converter
```

2. **Create virtual environment:**

```bash
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install in development mode:**

```bash
pip install -e '.[dev]'
```

Or use Make:

```bash
make install-dev
```

4. **Install pre-commit hooks (optional):**

```bash
pip install pre-commit
pre-commit install
```

## Project Structure

```
GP-Presets-Converter/
├── src/gp_presets_converter/    # Main package
│   ├── __init__.py
│   ├── cli.py                   # CLI interface
│   ├── converter.py             # Main converter class
│   ├── core/                    # Core modules
│   │   ├── analyzer.py
│   │   ├── converter.py
│   │   ├── parser.py
│   │   └── writer.py
│   ├── models/                  # Data models
│   │   ├── common.py
│   │   ├── gp5_preset.py
│   │   ├── gp50_preset.py
│   │   └── preset.py
│   ├── utils/                   # Utilities
│   │   ├── binary_parser.py
│   │   ├── file_handler.py
│   │   ├── hex_dump.py
│   │   └── validation.py
│   └── config/                  # Configuration
│       └── settings.py
├── tests/                       # Test suite
├── examples/                    # Usage examples
├── docs/                        # Documentation
└── pyproject.toml              # Project configuration
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

### 2. Make Changes

Follow the code style guidelines (see below).

### 3. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=gp_presets_converter --cov-report=html

# Run specific test
pytest tests/test_converter.py::TestPresetConverter::test_specific -v
```

### 4. Format and Lint Code

```bash
# Format code
black src/gp_presets_converter tests/
isort src/gp_presets_converter tests/

# Or use Make
make format

# Lint code
flake8 src/gp_presets_converter tests/
mypy src/gp_presets_converter

# Or use Make
make lint
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
# or
git commit -m "fix: fix bug description"
```

Use conventional commit messages:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `test:` for tests
- `refactor:` for code refactoring
- `style:` for formatting changes
- `chore:` for maintenance tasks

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style Guidelines

### Python Style

We follow PEP 8 with these specifics:

- **Line length:** 100 characters
- **Indentation:** 4 spaces
- **String quotes:** Double quotes preferred
- **Imports:** Grouped (stdlib, third-party, local)
- **Type hints:** Required for all functions

### Example Code Style

```python
"""Module docstring describing the module."""

from pathlib import Path
from typing import Optional, List

from .models import GP5Preset


def convert_preset(
    input_path: Path,
    output_path: Optional[Path] = None,
) -> List[Path]:
    """
    Convert a preset file.

    Args:
        input_path: Path to input file
        output_path: Optional output path

    Returns:
        List of converted file paths

    Raises:
        FileNotFoundError: If input doesn't exist
    """
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    # Implementation
    return []
```

### Docstring Style

Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When this happens
        TypeError: When that happens

    Example:
        >>> example_function("test", 42)
        True
    """
    pass
```

## Testing Guidelines

### Writing Tests

Tests should be:
- **Clear:** Descriptive test names
- **Isolated:** No dependencies between tests
- **Fast:** Quick to run
- **Comprehensive:** Cover edge cases

### Test Structure

```python
"""Tests for module_name."""

import pytest

from gp_presets_converter.module import ClassName


class TestClassName:
    """Test cases for ClassName."""

    def test_method_success_case(self):
        """Test that method works in normal case."""
        # Arrange
        obj = ClassName()

        # Act
        result = obj.method()

        # Assert
        assert result == expected

    def test_method_error_case(self):
        """Test that method raises error correctly."""
        obj = ClassName()

        with pytest.raises(ValueError, match="expected message"):
            obj.method_that_fails()

    def test_method_edge_case(self, tmp_path):
        """Test edge case with fixtures."""
        # Use tmp_path fixture for file operations
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")

        # Test logic
        ...
```

### Running Tests

```bash
# All tests
pytest tests/

# Specific file
pytest tests/test_converter.py

# Specific test
pytest tests/test_converter.py::TestPresetConverter::test_init

# With coverage
pytest tests/ --cov=gp_presets_converter

# With verbose output
pytest tests/ -v

# Stop on first failure
pytest tests/ -x
```

## Adding New Features

### 1. Plan the Feature

- Document the feature requirements
- Design the API
- Consider edge cases
- Plan tests

### 2. Implement Core Logic

Start with data models and core logic:

```python
# Add to src/gp_presets_converter/models/
class NewPresetModel:
    """New preset model."""
    pass

# Add to src/gp_presets_converter/core/
class NewConverter:
    """New converter logic."""
    pass
```

### 3. Add Tests

Write tests before or alongside implementation:

```python
# Add to tests/
class TestNewFeature:
    """Tests for new feature."""

    def test_basic_functionality(self):
        """Test basic use case."""
        pass

    def test_edge_cases(self):
        """Test edge cases."""
        pass
```

### 4. Update Documentation

- Update API reference
- Add usage examples
- Update README if needed

### 5. Create Example

Add example to `examples/usage_examples/`:

```python
#!/usr/bin/env python3
"""Example using new feature."""

from gp_presets_converter import NewFeature

# Demonstrate feature
...
```

## Debugging Tips

### Using Python Debugger

```python
import pdb; pdb.set_trace()  # Set breakpoint

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()
```

### VSCode Debugging

Launch configuration in `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Test",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v"]
        }
    ]
}
```

### Logging for Debugging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug information")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

## Common Development Tasks

### Add a New Effect Type

1. Add to `models/common.py`:
```python
@dataclass
class NewEffect(EffectParameters):
    """New effect parameters."""
    type: str = "new_effect"
    param1: float = 50.0
    param2: float = 50.0
```

2. Update conversion rules in `core/converter.py`
3. Add tests
4. Update documentation

### Add New Binary Parser Method

1. Add to `utils/binary_parser.py`:
```python
def read_custom_type(self) -> CustomType:
    """Read custom data type."""
    pass
```

2. Add tests in `tests/unit/test_binary_parser.py`
3. Document in API reference

### Add CLI Option

1. Update `cli.py`:
```python
parser.add_argument(
    "--new-option",
    action="store_true",
    help="Description of new option"
)
```

2. Handle the option in main()
3. Add tests in `tests/integration/test_cli.py`
4. Update usage documentation

## Making a Release

1. Update version in `pyproject.toml`
2. Update `__version__` in `src/gp_presets_converter/__init__.py`
3. Update CHANGELOG.md
4. Create git tag: `git tag v0.2.0`
5. Push tag: `git push origin v0.2.0`
6. Create GitHub release

## Getting Help

- Check existing issues on GitHub
- Ask in discussions
- Review code comments and docstrings
- Reach out to maintainers

## Code Review Checklist

Before submitting PR, ensure:

- [ ] All tests pass
- [ ] Code is formatted (black, isort)
- [ ] No linting errors (flake8, mypy)
- [ ] Documentation updated
- [ ] Examples added if applicable
- [ ] Changelog updated
- [ ] Commit messages follow convention

Thank you for contributing!

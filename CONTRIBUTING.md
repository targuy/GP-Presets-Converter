# Contributing to GP Presets Converter

Thank you for your interest in contributing to GP Presets Converter!

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Git

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/targuy/GP-Presets-Converter.git
cd GP-Presets-Converter
```

2. Run the setup script:
```bash
./setup.sh
```

Or manually set up:
```bash
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e '.[dev]'
```

## Development Workflow

### Running Tests

```bash
make test
# or
pytest tests/ -v
```

### Code Formatting

This project uses `black` and `isort` for code formatting:

```bash
make format
# or
black src/ tests/
isort src/ tests/
```

### Linting

```bash
make lint
# or
flake8 src/ tests/ --max-line-length=100
mypy src/gp_presets_converter
```

### Running the CLI

```bash
gp-convert <input-file>
# or
python -m gp_presets_converter.cli <input-file>
```

## Project Structure

```
GP-Presets-Converter/
├── src/gp_presets_converter/  # Main package source code
│   ├── __init__.py           # Package initialization
│   ├── converter.py          # Core conversion logic
│   └── cli.py                # Command-line interface
├── tests/                     # Test suite
│   ├── __init__.py
│   └── test_converter.py
├── .vscode/                   # VSCode configuration
├── .devcontainer/            # GitHub Codespaces configuration
├── pyproject.toml            # Project metadata and dependencies
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── Makefile                  # Development commands
└── setup.sh                  # Environment setup script
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes
- Write tests for new features

## Pull Request Process

1. Create a new branch for your feature or bugfix
2. Write tests for your changes
3. Ensure all tests pass: `make test`
4. Format your code: `make format`
5. Run linters: `make lint`
6. Commit your changes with clear commit messages
7. Push to your fork and submit a pull request

## Questions?

Feel free to open an issue for any questions or concerns.

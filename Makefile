.PHONY: help install install-dev test lint format clean run

help:
	@echo "GP Presets Converter - Makefile Commands"
	@echo "========================================="
	@echo "make install      - Install the package in production mode"
	@echo "make install-dev  - Install the package in development mode with dev dependencies"
	@echo "make test         - Run tests with pytest"
	@echo "make lint         - Run linters (flake8, mypy)"
	@echo "make format       - Format code with black and isort"
	@echo "make clean        - Remove build artifacts and cache files"
	@echo "make run          - Run the CLI (requires INPUT variable)"

install:
	pip install -e .

install-dev:
	pip install -e '.[dev]'

test:
	pytest tests/ -v --cov=gp_presets_converter --cov-report=term-missing

lint:
	flake8 src/gp_presets_converter tests/
	mypy src/gp_presets_converter

format:
	black src/gp_presets_converter tests/
	isort src/gp_presets_converter tests/

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	@if [ -z "$(INPUT)" ]; then \
		echo "Error: Please specify INPUT variable (e.g., make run INPUT=file.gp5)"; \
		exit 1; \
	fi
	python -m gp_presets_converter.cli $(INPUT)

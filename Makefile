.PHONY: help install install-dev clean test lint format

help:
@echo "ModPocket Monorepo Commands:"
@echo "  make install        - Install all packages"
@echo "  make install-dev    - Install all packages in development mode with dev dependencies"
@echo "  make clean          - Clean build artifacts"
@echo "  make test           - Run tests for all packages"
@echo "  make lint           - Lint all packages"
@echo "  make format         - Format all packages"

install:
pip install -e packages/core
pip install -e packages/utils
pip install -e packages/api

install-dev:
pip install -e packages/core[dev]
pip install -e packages/utils[dev]
pip install -e packages/api[dev]

clean:
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

test:
pytest packages/

lint:
ruff check packages/

format:
ruff format packages/

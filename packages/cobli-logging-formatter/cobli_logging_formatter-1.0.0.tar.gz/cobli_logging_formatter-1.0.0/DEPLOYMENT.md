# Cobli Logging Formatter - Deployment Guide

## Overview

This package provides a production-ready, structured JSON logging formatter with Datadog integration for Python applications. It's designed to be easily distributed and integrated within your company's codebase.

## Package Structure

```
cobli-logging-formatter/
├── cobli_logging/              # Main package
│   ├── __init__.py            # Package exports
│   ├── formatter.py           # JsonFormatter class
│   └── config.py              # Configuration utilities
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_logging.py
├── examples/                   # Usage examples
│   └── usage_examples.py
├── setup.py                   # Package setup
├── pyproject.toml             # Modern Python packaging
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
├── LICENSE                    # MIT License
├── MANIFEST.in               # Package manifest
└── .gitignore                # Git ignore rules
```

## Distribution Options

### Option 1: Internal PyPI Server
If your company has an internal PyPI server:

```bash
# Build the package
uv build

# Upload to internal PyPI (using twine)
uv run twine upload --repository-url https://your-internal-pypi.com dist/*
```

### Option 2: Git Repository
Distribute via Git repository:

```bash
# Install directly from Git with uv
uv add git+https://github.com/your-company/cobli-logging-formatter.git

# Or with specific version
uv add git+https://github.com/your-company/cobli-logging-formatter.git@v1.0.0

# Or with pip
pip install git+https://github.com/your-company/cobli-logging-formatter.git
pip install git+https://github.com/your-company/cobli-logging-formatter.git@v1.0.0
```

### Option 3: Wheel Distribution
Build and distribute wheel files:

```bash
# Build wheel with uv
uv build --wheel

# Distribute the .whl file from dist/ directory
uv add ./dist/cobli_logging_formatter-1.0.0-py3-none-any.whl
# Or with pip
pip install dist/cobli_logging_formatter-1.0.0-py3-none-any.whl
```

## Installation for End Users

Using uv (recommended):
```bash
uv add cobli-logging-formatter
```

Or with pip:
```bash
pip install cobli-logging-formatter
```

## Quick Usage

### Minimal Setup
```python
from cobli_logging import get_logger

logger = get_logger()
logger.info("Application started")
```

### With Custom Configuration
```python
from cobli_logging import configure_logging

logger = configure_logging(
    service_name="my-service",
    version="1.2.0",
    log_level="DEBUG"
)
logger.info("Custom configured logger")
```

### Using Just the Formatter
```python
import logging
from cobli_logging import JsonFormatter

logger = logging.getLogger("my-app")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
```

## Environment Variables

- `DD_SERVICE`: Service name for Datadog
- `DD_VERSION`: Service version for Datadog  
- `LOG_LEVEL`: Logging level (default: "INFO")

## Features

✅ **Structured JSON Output**: Consistent, parseable log format
✅ **Datadog Integration**: Automatic trace/span ID inclusion
✅ **Custom Fields**: Supports extra log data
✅ **Thread Safety**: Safe for multi-threaded applications
✅ **Exception Handling**: Captures stack traces
✅ **Zero Configuration**: Works out of the box
✅ **Flexible Setup**: Multiple configuration options
✅ **Production Ready**: Comprehensive error handling

## Development

Using uv (recommended):
```bash
# Clone and setup
git clone <repository>
cd cobli-logging-formatter

# Initialize with uv and install dependencies
uv sync --dev

# Install in development mode (editable install)
uv pip install -e .

# Run tests
uv run python -m pytest

# Format code
uv run python -m black .

# Lint
uv run python -m flake8 cobli_logging/ --max-line-length=88
```

Or with pip:
```bash
# Clone and setup
git clone <repository>
cd cobli-logging-formatter

# Install in development mode
pip install -e .

# Run tests
pytest

# Format code
black .

# Lint
flake8 cobli_logging/
```

## Migration from Existing Code

To migrate from your existing `logging.py` file:

1. **Replace imports:**
   ```python
   # Old
   from logging import logger
   
   # New
   from cobli_logging import get_logger
   logger = get_logger()
   ```

2. **Update configuration:**
   ```python
   # Old
   logger = logging.getLogger(os.environ.get('DD_SERVICE'))
   # ... manual setup
   
   # New
   from cobli_logging import configure_logging
   logger = configure_logging()
   ```

3. **Keep existing log calls unchanged:**
   ```python
   # These remain the same
   logger.info("Message")
   logger.error("Error", extra={"user_id": 123})
   ```

## Support

For issues and questions, contact the development team or create an issue in the internal repository.

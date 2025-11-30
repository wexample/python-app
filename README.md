# wexample-app

Version: 0.0.68

Helpers for building Python app or cli.

## Table of Contents

- [Status Compatibility](#status-compatibility)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Basic Usage](#basic-usage)
- [Configuration](#configuration)
- [Logging](#logging)
- [Api Reference](#api-reference)
- [Examples](#examples)
- [Tests](#tests)
- [Code Quality](#code-quality)
- [Versioning](#versioning)
- [Troubleshooting](#troubleshooting)
- [Compatibility Matrix](#compatibility-matrix)
- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Links](#links)


## Status & Compatibility

**Maturity**: Production-ready

**Python Support**: >=3.10

**OS Support**: Linux, macOS, Windows

**Status**: Actively maintained

## Prerequisites

No special system dependencies required beyond Python >=3.10.

## Installation

```bash
pip install wexample-app
```

## Quickstart

Get started with **wexample-app** in seconds:

```python
# Your first example with wexample-app
from wexample-app import YourClass

# Initialize and use
instance = YourClass()
instance.run()
```

This package requires Python >=3.10.

## Basic Usage

```python
from wexample_helpers.decorator.base_class import base_class

from wexample_app.common.abstract_kernel import AbstractKernel
from wexample_app.common.mixins.command_line_kernel import CommandLineKernel
from wexample_app.common.mixins.command_runner_kernel import CommandRunnerKernel

@base_class
class MyApp(CommandRunnerKernel, CommandLineKernel, AbstractKernel):
    pass

my_app = MyApp()
```

## Configuration

Configuration can be provided through environment variables or config files.

### Environment Variables

- `WEXAMPLE-APP_DEBUG`: Enable debug mode
- `WEXAMPLE-APP_LOG_LEVEL`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## Logging & Verbosity Control

Control logging output with environment variables:

```bash
export WEXAMPLE-APP_LOG_LEVEL=DEBUG
```

Or programmatically:

```python
import logging
logging.getLogger('wexample-app').setLevel(logging.DEBUG)
```

## API Reference

Full API documentation is available in the source code docstrings.

Key modules and classes are documented with type hints for better IDE support.

## Additional Examples

### Advanced Usage

```python
from wexample-app import AdvancedFeature

# Advanced example
feature = AdvancedFeature(config={'option': 'value'})
result = feature.execute()
```

More examples can be found in the `examples/` directory of the repository.

## Tests

Run the test suite:

```bash
pytest tests/
```

With coverage:

```bash
pytest --cov=wexample-app tests/
```

## Code Quality & Typing

All the suite packages follow strict quality standards:

- **Type hints**: Full type coverage with mypy validation
- **Code formatting**: Enforced with black and isort
- **Linting**: Comprehensive checks with custom scripts and tools
- **Testing**: High test coverage requirements

These standards ensure reliability and maintainability across the suite.

## Versioning & Compatibility Policy

Wexample packages follow **Semantic Versioning** (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

We maintain backward compatibility within major versions and provide clear migration guides for breaking changes.

## Troubleshooting & FAQ

### Common Issues

**Q: Installation fails with dependency errors**  
A: Ensure you're using Python >=3.10 and have the latest pip version.

**Q: Import errors**  
A: Verify the package is installed: `pip show wexample-app`

For more help, see the [Support Channels](#support-channels) section.

## Compatibility Matrix

This package is part of the Wexample suite and is compatible with other suite packages.

Refer to each package's documentation for specific version compatibility requirements.

## Requirements

- Python >=3.10

## Dependencies

- attrs>=23.1.0
- cattrs>=23.1.0
- dotenv
- python-dotenv
- wexample-filestate==0.0.71
- wexample-helpers-yaml==0.0.110

## Links

- Homepage: https://github.com/wexample/python-app


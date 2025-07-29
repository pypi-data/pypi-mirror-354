# good-dev

Development tools and CLI utilities for managing good-* packages.

## Installation

```bash
pip install good-dev
```

## Features

### Dependency Explorer

good-dev includes a comprehensive dependency exploration toolset to help you discover functionality within your existing dependencies before adding new ones.

#### Commands

**Tree View**
```bash
# Show dependency tree for a specific package
good-dev packages tree requests --max-depth 3

# Show dependency tree for current project
good-dev packages tree
```

**Search Dependencies**
```bash
# Search for functionality across all dependencies
good-dev packages search "json" --type function

# Search in a specific package
good-dev packages search "parse" --package urllib3 --type class
```

**API Discovery**
```bash
# List all APIs exported by a package
good-dev packages api requests

# Filter APIs by pattern
good-dev packages api json --filter "dump"
```

**Community Explorer**
```bash
# Find packages that share dependencies
good-dev packages community fastapi pydantic --min-overlap 2

# Discover packages in the data science ecosystem
good-dev packages community pandas numpy --limit 20
```

### Configuration Management

```bash
# Manage application configuration
good-dev config set my_key my_value
good-dev config get my_key
```

### Package Analysis

```bash
# Get reverse dependencies for packages
good-dev packages reverse-dependencies requests typer
```

### Run Utilities

```bash
# Execute arbitrary Python functions
good-dev run path.to.module:function --arg1 value1
```

## Development

This package is part of the good-libraries monorepo. To contribute:

1. Clone the repository
2. Navigate to `libs/good-dev`
3. Install dependencies with `uv sync`
4. Run tests with `uv run pytest`

## Dependencies

- `typer`: CLI framework
- `rich`: Beautiful terminal formatting
- `httpx`: HTTP client
- `cashews`: Caching library
- `loguru`: Logging
- And more...
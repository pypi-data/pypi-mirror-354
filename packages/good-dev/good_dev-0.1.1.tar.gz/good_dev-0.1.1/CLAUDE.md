# Good Dev Library

Development tools and CLI utilities for Good Kiwi projects, providing a command-line interface for common development tasks.

## Package Overview

good-dev is a CLI tool built with Typer that provides utilities for managing Good Kiwi projects. It includes configuration management, package operations, and development workflow helpers.

## Installation & Usage

Once installed, the CLI is available as `good-dev`:

```bash
good-dev --help
good-dev config show
good-dev packages list
```

## Key Components

### CLI Structure (`cli/`)
- Built on Typer for a modern CLI experience
- Modular command structure under `cli/commands/`
- Rich formatting for better terminal output

### Commands

#### Config Command (`commands/config.py`)
- Manage project configuration
- Read/write TOML configuration files
- Environment-specific settings

#### Packages Command (`commands/packages.py`)
- Package management utilities
- Dependency tracking
- Version management

#### Run Command (`commands/run.py`)
- Execute common development tasks
- Script runner functionality
- Process management

### Configuration (`config.py`)
- TOML-based configuration
- Hierarchical settings management
- Environment variable support

### Utilities (`utilities.py`)
- Common helper functions
- File operations
- Path management

### Wheelodex Integration (`tools/wheelodex/`)
- Python wheel package analysis
- API client for wheelodex service
- Package metadata extraction

## Configuration

The tool uses TOML configuration files:

```toml
[project]
name = "my-project"
version = "0.1.0"

[development]
debug = true
log_level = "DEBUG"

[production]
debug = false
log_level = "INFO"
```

## Command Examples

### Configuration Management
```bash
# Show current configuration
good-dev config show

# Set a configuration value
good-dev config set development.debug true

# Get a specific value
good-dev config get project.name
```

### Package Operations
```bash
# List all packages
good-dev packages list

# Show package info
good-dev packages info good-common

# Check dependencies
good-dev packages deps
```

### Running Tasks
```bash
# Run a predefined task
good-dev run test

# Execute with options
good-dev run build --env production
```

## Extending the CLI

Add new commands by creating a module under `cli/commands/`:

```python
# cli/commands/mycommand.py
import typer

app = typer.Typer()

@app.command()
def hello(name: str = "World"):
    """Say hello"""
    typer.echo(f"Hello {name}!")

# Register in cli/__init__.py
```

## Dependencies

- `typer`: Modern CLI framework
- `rich`: Terminal formatting
- `toml`: Configuration file format
- `cashews`: Caching functionality
- `diskcache`: Persistent caching
- `httpx`: HTTP client for API calls

## Development Workflow

This tool is designed to streamline common development tasks:

1. **Project Setup**: Initialize configuration
2. **Dependency Management**: Track and update dependencies
3. **Task Automation**: Run common tasks with single commands
4. **Package Analysis**: Understand package structure and dependencies

## Best Practices

1. Keep configuration in version control
2. Use environment-specific config files
3. Document custom commands and tasks
4. Leverage caching for expensive operations
5. Use the wheelodex integration for package insights

## Future Enhancements

The tool is designed to be extensible. Common additions might include:
- Test runners
- Deployment commands  
- Database migrations
- Code generation
- Linting and formatting
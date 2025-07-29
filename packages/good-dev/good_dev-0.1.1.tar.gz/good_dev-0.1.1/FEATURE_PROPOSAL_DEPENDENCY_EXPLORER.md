# Feature Proposal: Dependency Explorer for good-dev

## Executive Summary

Add a comprehensive dependency exploration toolset to good-dev that enables developers to discover and understand functionality within their existing dependencies before adding new ones. This tool will help reduce dependency bloat by leveraging the transitive dependencies already present in well-established packages.

## Problem Statement

Modern Python projects often accumulate unnecessary dependencies because developers are unaware of functionality already available in their dependency tree. Well-established packages like Django, FastAPI, or SQLAlchemy bring in carefully chosen, well-maintained dependencies that have already solved common problems. By exploring these existing dependencies first, developers can:

- Reduce security surface area
- Minimize version conflicts
- Decrease project complexity
- Leverage battle-tested solutions

## Proposed Solution

### Core Features

#### 1. Dependency Tree Explorer
- **Command**: `good-dev packages tree [package-name]`
- Parse `uv.lock` and `pyproject.toml` to build complete dependency graph
- Show transitive dependencies with version constraints
- Highlight shared dependencies across packages
- Export to various formats (JSON, tree view, GraphViz)

#### 2. Code Search Within Dependencies
- **Command**: `good-dev packages search <pattern> [--type function|class|import]`
- Search for functionality across all installed packages
- Use AST parsing for semantic search (functions, classes, decorators)
- Regex support for pattern matching
- Show code snippets with context

#### 3. API Discovery
- **Command**: `good-dev packages api <package-name> [--filter pattern]`
- List all public APIs exported by a package
- Show function signatures and docstrings
- Filter by name pattern or type
- Export to markdown for documentation

#### 4. Documentation Aggregator
- **Command**: `good-dev packages docs <package-name> [--section pattern]`
- Fetch documentation from multiple sources:
  - PyPI package description
  - GitHub README and docs
  - Inline docstrings
  - ReadTheDocs if available
- Cache documentation locally for offline access
- Search within documentation

#### 5. Dependency Health Check
- **Command**: `good-dev packages health [--security --maintenance --popularity]`
- Check for security vulnerabilities (via safety or pip-audit)
- Show maintenance status (last update, open issues)
- Display popularity metrics (downloads, stars)
- Identify outdated or abandoned packages

#### 6. Dependency Community Explorer (leveraging existing wheelodex tool)
- **Command**: `good-dev packages community <package-names> [--min-overlap 2]`
- Find packages that depend on your existing dependencies
- Discover package "communities" (e.g., packages using both Pydantic and FastAPI)
- Use cases:
  - Find compatible libraries in your ecosystem
  - Discover well-integrated solutions
  - Identify popular package combinations
- **Improvements to existing wheelodex implementation**:
  - Add comprehensive caching for reverse dependency lists (current implementation fetches from API each time)
  - Cache complete dependency graphs with longer TTL (14 days for stable packages)
  - Implement tiered caching based on package popularity
  - Add `force_refresh` parameter for cache bypass
  - Background refresh for frequently accessed data

Example workflow:
```bash
# Find packages that use both FastAPI and Pydantic
$ good-dev packages community fastapi pydantic --min-overlap 2
Found 47 packages using both fastapi and pydantic:
- sqlmodel: SQL databases with FastAPI and Pydantic
- fastapi-users: Ready-to-use user management
- ormar: Async ORM built on SQLAlchemy core
...

# Find packages in the "data science" community
$ good-dev packages community pandas numpy scikit-learn --min-overlap 2
Found 132 packages in the data science ecosystem:
- seaborn: Statistical data visualization
- xarray: N-dimensional labeled arrays
- dask: Parallel computing with task scheduling
...
```

### Claude Code Integration

#### Option 1: MCP Service (Recommended)
Create a Model Context Protocol service that exposes dependency data:

```python
# mcp_server.py
@server.tool()
async def search_dependencies(query: str, search_type: str = "all"):
    """Search for functionality within project dependencies"""
    ...

@server.tool()
async def get_dependency_tree(package: str = None):
    """Get the dependency tree for current project or specific package"""
    ...

@server.tool()
async def find_api(functionality: str):
    """Find APIs that provide specific functionality"""
    ...

@server.tool()
async def explore_community(packages: list[str], min_overlap: int = 2):
    """Find packages that share dependencies with given packages"""
    ...
```

#### Option 2: Pipeable CLI
Design commands to output structured JSON for easy piping:

```bash
# Find all CSV parsing functionality
good-dev packages search "csv|CSV" --type class --json | claude-code "Which CSV parser should I use?"

# Get dependency tree for analysis
good-dev packages tree --json | claude-code "Are there any redundant dependencies?"
```

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1-2)
- [ ] Add dependency tree parser using `importlib.metadata` and `uv` APIs
- [ ] Create abstract search interface for different search strategies
- [ ] Implement caching layer for package metadata (extend existing cache)
- [ ] Add JSON output formatters for all commands
- [ ] **Enhance wheelodex caching**: Add dedicated cache for complete reverse dependency lists

### Phase 2: Search Capabilities (Week 3-4)
- [ ] Implement AST-based code search using `ast` module
- [ ] Add ripgrep integration for fast text search
- [ ] Create API discovery using `inspect` and `importlib`
- [ ] Build search index for installed packages

### Phase 3: Documentation & Health (Week 5-6)
- [ ] Integrate PyPI JSON API for package metadata
- [ ] Add GitHub API integration for README/docs
- [ ] Implement vulnerability checking (safety/pip-audit)
- [ ] Create documentation cache and search

### Phase 4: Community Explorer (Week 7-8)
- [ ] Refactor wheelodex caching with tiered TTL strategy
- [ ] Implement community discovery algorithm
- [ ] Add graph visualization for package relationships
- [ ] Create recommendation engine for compatible packages
- [ ] Add cache warming for popular package combinations

### Phase 5: Claude Code Integration (Week 9-10)
- [ ] Design and implement MCP service
- [ ] Create example prompts and workflows
- [ ] Add structured output formats for LLM consumption
- [ ] Write integration documentation

## Technical Architecture

### Dependencies to Add
```toml
[dependencies]
# Existing deps...
importlib-metadata = ">=4.0"  # For package introspection
rich = ">=12.0"  # For beautiful tree visualization
networkx = ">=2.0"  # For dependency graph analysis
safety = { version = ">=2.0", optional = true }  # For security checks
aiofiles = ">=0.8"  # For async file operations

[optional-dependencies]
mcp = ["mcp-server", "fastapi", "uvicorn"]  # For MCP service
```

### Data Models
```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class PackageInfo(BaseModel):
    name: str
    version: str
    dependencies: List['PackageInfo']
    metadata: Dict[str, Any]
    apis: List['APIInfo']
    
class APIInfo(BaseModel):
    name: str
    type: str  # function, class, constant
    signature: Optional[str]
    docstring: Optional[str]
    module: str
    
class SearchResult(BaseModel):
    package: str
    module: str
    line: int
    context: str
    match_type: str
```

### Integration with Existing Code

Extend the existing `packages.py` command group:

```python
# libs/good-dev/src/good_dev/cli/commands/packages.py

@app.command()
async def tree(
    package: Optional[str] = None,
    max_depth: int = 3,
    show_versions: bool = True,
    output_format: str = "tree"  # tree, json, dot
):
    """Show dependency tree for current project or specific package"""
    ...

@app.command()
async def search(
    pattern: str,
    search_type: str = "all",  # all, function, class, import
    case_sensitive: bool = False,
    output_format: str = "table"  # table, json, code
):
    """Search for functionality within installed dependencies"""
    ...

@app.command()
async def community(
    packages: List[str],
    min_overlap: int = 2,
    limit: int = 50,
    output_format: str = "table",  # table, json, graph
    force_refresh: bool = False
):
    """Find packages that share dependencies with given packages
    
    Leverages the existing wheelodex reverse dependency data
    with enhanced caching for better performance.
    """
    ...
```

## Example Usage Scenarios

### Scenario 1: Finding CSV Processing
```bash
$ good-dev packages search "csv" --type module
Found 5 packages with CSV functionality:
- pandas: High-performance CSV reading/writing
- csv (stdlib): Built-in CSV module
- openpyxl: Excel/CSV compatibility
...

$ good-dev packages api pandas --filter "read_csv"
pandas.read_csv(filepath_or_buffer, sep=',', ...) -> DataFrame
    Read a comma-separated values (csv) file into DataFrame.
```

### Scenario 2: Understanding Dependencies
```bash
$ good-dev packages tree requests
requests==2.31.0
├── charset-normalizer>=2,<4
├── idna>=2.5,<4
├── urllib3>=1.21.1,<3
└── certifi>=2017.4.17

$ good-dev packages health
✓ All dependencies up to date
⚠ urllib3: Security advisory CVE-2023-XXXX (fixed in 2.0.7)
✓ No abandoned packages detected
```

### Scenario 3: Exploring Package Communities
```bash
$ good-dev packages community fastapi sqlalchemy --min-overlap 2
Analyzing package ecosystem...
Found 23 packages using both fastapi and sqlalchemy:

High-quality integrations (★ = 1000+ users):
- sqlmodel ★★★★★: SQL databases with FastAPI and Pydantic
- fastapi-sqlalchemy ★★★: SQLAlchemy session management
- fastapi-utils ★★★: Reusable utilities for FastAPI
- databases ★★★: Async database support

Specialized solutions:
- fastapi-crudrouter: Automatic CRUD route generation
- fastapi-pagination: Easy pagination for SQLAlchemy
- fastapi-async-sqlalchemy: Async SQLAlchemy integration

$ good-dev packages community pydantic mypy --output-format json | \
  claude-code "What are the best type-safe data validation libraries?"
```

### Scenario 4: Claude Code Integration
```bash
# As MCP service
$ good-dev mcp serve

# In Claude Code
> "Find me a way to parse YAML files without adding a new dependency"
[Claude Code queries MCP service, finds PyYAML in dependencies]
"You already have PyYAML 6.0 installed as a dependency of docker-compose..."

# As CLI pipe
$ good-dev packages search "cache" --json | claude-code \
  "Which caching solution should I use for my use case?"
```

## Success Metrics

1. **Dependency Reduction**: Track if projects using this tool add fewer dependencies
2. **Discovery Rate**: Measure how often developers find existing solutions
3. **Performance**: Search operations complete in <2 seconds for typical projects
4. **Adoption**: Integration with Claude Code leads to 50%+ usage in good-* projects

## Open Questions

1. Should we build our own AST parser or leverage existing tools like `rope` or `jedi`?
2. How deep should security scanning go? Just direct dependencies or full tree?
3. Should we maintain a central index of common functionality mappings?
4. What's the best way to handle C extensions that can't be parsed?

## Alternatives Considered

### Using Existing Tools
- **pipdeptree**: Good for dependency trees but lacks search functionality
- **pip-audit**: Handles security but not discovery
- **pydoc**: Limited to documentation, no code search
- **grep/ripgrep**: Fast but not Python-aware

**Decision**: Build on top of these tools rather than replacing them. Use pipdeptree's tree algorithms, integrate pip-audit for security, and use ripgrep for initial search with AST parsing for refinement.

### Different Integration Approaches
- **VS Code Extension**: More integrated but limited to one editor
- **GitHub Action**: Good for CI but not interactive exploration
- **Jupyter Extension**: Limited to notebook users

**Decision**: MCP service provides the most flexibility and can be adapted to multiple interfaces.

## Conclusion

This dependency explorer will make good-dev an essential tool for Python developers who want to write leaner, more maintainable code. By surfacing the wealth of functionality already available in their dependency tree, developers can make more informed decisions about when to add new dependencies versus leveraging existing ones.

The tight integration with Claude Code through MCP will make this particularly powerful for AI-assisted development, where the LLM can help developers discover and understand existing functionality before suggesting new dependencies.
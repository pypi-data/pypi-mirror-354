import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from good_dev.tools.wheelodex import build_dependency_graph
from good_dev.tools.dependency_explorer import DependencyExplorer
from good_common.utilities import yaml_dump

# from fast_depends import Depends, inject

console = Console()
app = typer.Typer()

# @app.callback()
# def main():
#     typer.echo('main command')


@app.command()
def reverse_dependencies(
    packages: list[str] = typer.Argument(
        ..., help="List of packages to get reverse dependencies for"
    ),
    output: Path = typer.Option(
        "dependencies.yaml", help="Output file to write the dependency graph to"
    ),
):
    typer.echo(f"Getting reverse dependencies for {packages}")

    with asyncio.Runner() as runner:
        dependency_graph = runner.run(build_dependency_graph(packages))

    yaml_dump(output, dependency_graph)


@app.command()
def tree(
    package: Optional[str] = typer.Argument(
        None, help="Package name to show dependencies for. If not provided, shows project dependencies"
    ),
    max_depth: int = typer.Option(
        3, "--max-depth", "-d", help="Maximum depth to traverse"
    ),
    show_versions: bool = typer.Option(
        True, "--show-versions/--no-versions", help="Show package versions"
    ),
    output_format: str = typer.Option(
        "tree", "--format", "-f", help="Output format: tree, json, or yaml"
    ),
):
    """Show dependency tree for current project or specific package."""
    explorer = DependencyExplorer()
    
    if package:
        tree_data = explorer.build_dependency_tree(package, max_depth, show_versions)
    else:
        # Show project dependencies
        project_deps = explorer.get_project_dependencies()
        tree_data = {
            'name': 'Project Dependencies',
            'source': project_deps['source'],
            'dependencies': []
        }
        
        for dep in project_deps['dependencies']:
            dep_name = dep.split('[')[0].split('<')[0].split('>')[0].split('=')[0].strip()
            if dep_name:
                child = explorer.build_dependency_tree(dep_name, max_depth - 1, show_versions)
                tree_data['dependencies'].append(child)
    
    # Output in requested format
    if output_format == "json":
        console.print_json(json.dumps(tree_data, indent=2))
    elif output_format == "yaml":
        console.print(yaml_dump(None, tree_data))
    else:
        # Tree format
        tree = Tree(f"[bold]{tree_data['name']}[/bold]")
        if 'version' in tree_data:
            tree.label += f" [dim]({tree_data['version']})[/dim]"
        if 'source' in tree_data:
            tree.label += f" [dim italic]from {tree_data['source']}[/dim italic]"
            
        _add_tree_nodes(tree, tree_data.get('dependencies', []))
        console.print(tree)


def _add_tree_nodes(tree: Tree, dependencies: list, prefix: str = ""):
    """Helper to recursively add nodes to rich tree."""
    for dep in dependencies:
        label = f"{dep['name']}"
        if 'version' in dep:
            label += f" [dim]({dep['version']})[/dim]"
        if dep.get('circular'):
            label += " [red](circular)[/red]"
        elif dep.get('truncated'):
            label += " [yellow](...)[/yellow]"
            
        node = tree.add(label)
        if 'dependencies' in dep:
            _add_tree_nodes(node, dep['dependencies'])


@app.command()
def search(
    pattern: str = typer.Argument(..., help="Search pattern (regex)"),
    package: Optional[str] = typer.Option(
        None, "--package", "-p", help="Search in specific package only"
    ),
    search_type: str = typer.Option(
        "all", "--type", "-t", help="Search type: all, function, class, or import"
    ),
    case_sensitive: bool = typer.Option(
        False, "--case-sensitive", "-c", help="Case sensitive search"
    ),
    max_results: int = typer.Option(
        50, "--max-results", "-m", help="Maximum number of results"
    ),
    output_format: str = typer.Option(
        "table", "--format", "-f", help="Output format: table or json"
    ),
):
    """Search for functionality within installed dependencies."""
    explorer = DependencyExplorer()
    
    console.print(f"[bold]Searching for pattern:[/bold] {pattern}")
    if package:
        console.print(f"[bold]In package:[/bold] {package}")
    console.print()
    
    results = explorer.search_package_code(
        pattern, package, search_type, case_sensitive, max_results
    )
    
    if output_format == "json":
        console.print_json(json.dumps(results, indent=2))
    else:
        if not results:
            console.print("[yellow]No results found[/yellow]")
            return
            
        table = Table(title=f"Found {len(results)} results")
        table.add_column("Package", style="cyan")
        table.add_column("File", style="green")
        table.add_column("Line", style="yellow")
        table.add_column("Type", style="magenta")
        table.add_column("Content", style="white")
        
        for result in results:
            content = result.get('content', '')
            if 'info' in result:
                info = result['info']
                if result['type'] == 'function':
                    content = info.get('signature', info.get('name', ''))
                elif result['type'] == 'class':
                    content = f"class {info.get('name', '')}({', '.join(info.get('bases', []))})"
                elif result['type'] == 'import':
                    content = info.get('import', '')
                    
            table.add_row(
                result['package'],
                result['file'][-50:] if len(result['file']) > 50 else result['file'],
                str(result['line']),
                result.get('type', 'text'),
                content[:80] + '...' if len(content) > 80 else content
            )
            
        console.print(table)


@app.command()
def api(
    package: str = typer.Argument(..., help="Package name to inspect"),
    filter_pattern: Optional[str] = typer.Option(
        None, "--filter", "-f", help="Filter APIs by pattern (regex)"
    ),
    include_private: bool = typer.Option(
        False, "--private", "-p", help="Include private APIs (starting with _)"
    ),
    output_format: str = typer.Option(
        "table", "--format", help="Output format: table or json"
    ),
):
    """List APIs exported by a package."""
    explorer = DependencyExplorer()
    
    console.print(f"[bold]Package:[/bold] {package}")
    if filter_pattern:
        console.print(f"[bold]Filter:[/bold] {filter_pattern}")
    console.print()
    
    apis = explorer.find_package_apis(package, include_private, filter_pattern)
    
    if output_format == "json":
        console.print_json(json.dumps(apis, indent=2))
    else:
        if not apis:
            console.print("[yellow]No APIs found or package cannot be imported[/yellow]")
            return
            
        table = Table(title=f"{package} APIs ({len(apis)} found)")
        table.add_column("Name", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Signature", style="yellow")
        table.add_column("Description", style="white")
        
        for api in apis:
            desc = api.get('doc', '')
            if desc:
                # Get first line of docstring
                desc = desc.split('\n')[0][:60]
                if len(api.get('doc', '')) > 60:
                    desc += '...'
                    
            table.add_row(
                api['name'],
                api['type'],
                api.get('signature', ''),
                desc
            )
            
        console.print(table)


@app.command()
def community(
    packages: list[str] = typer.Argument(
        ..., help="List of packages to find community for"
    ),
    min_overlap: int = typer.Option(
        2, "--min-overlap", "-m", help="Minimum number of packages that must overlap"
    ),
    limit: int = typer.Option(
        50, "--limit", "-l", help="Maximum number of results to show"
    ),
    output_format: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json, or yaml"
    ),
    force_refresh: bool = typer.Option(
        False, "--force-refresh", help="Force refresh of cached data"
    ),
):
    """Find packages that share dependencies with given packages.
    
    This helps discover package "communities" - packages that work well together
    because they share common dependencies.
    """
    console.print(f"[bold]Finding community for:[/bold] {', '.join(packages)}")
    console.print(f"[bold]Minimum overlap:[/bold] {min_overlap}")
    console.print()
    
    # For now, use the existing reverse dependencies functionality
    # In the future, this will be enhanced with better caching
    with asyncio.Runner() as runner:
        dependency_graph = runner.run(build_dependency_graph(packages))
    
    # Find packages that appear in multiple reverse dependency lists
    package_counts = {}
    package_info = {}
    
    for pkg, data in dependency_graph.items():
        if 'rdepends' in data:
            for rdep in data['rdepends']:
                rdep_name = rdep['name']
                package_counts[rdep_name] = package_counts.get(rdep_name, 0) + 1
                package_info[rdep_name] = rdep
    
    # Filter by minimum overlap
    community = [
        (name, info, count) 
        for name, count in package_counts.items() 
        if count >= min_overlap
        for info in [package_info[name]]
    ]
    
    # Sort by count and limit
    community.sort(key=lambda x: (-x[2], x[0]))
    community = community[:limit]
    
    if output_format == "json":
        result = [
            {
                'name': name,
                'shared_dependencies': count,
                'info': info
            }
            for name, info, count in community
        ]
        console.print_json(json.dumps(result, indent=2))
    elif output_format == "yaml":
        result = {
            name: {
                'shared_dependencies': count,
                'info': info
            }
            for name, info, count in community
        }
        console.print(yaml_dump(None, result))
    else:
        if not community:
            console.print("[yellow]No packages found with sufficient overlap[/yellow]")
            return
            
        table = Table(title=f"Package Community ({len(community)} packages)")
        table.add_column("Package", style="cyan")
        table.add_column("Shared", style="green")
        table.add_column("Description", style="white")
        table.add_column("Downloads", style="yellow")
        
        for name, info, count in community:
            desc = info.get('summary', '')[:60]
            if len(info.get('summary', '')) > 60:
                desc += '...'
                
            downloads = info.get('downloads', {}).get('recent', 0)
            if downloads > 1_000_000:
                downloads_str = f"{downloads / 1_000_000:.1f}M"
            elif downloads > 1_000:
                downloads_str = f"{downloads / 1_000:.1f}K"
            else:
                downloads_str = str(downloads)
                
            table.add_row(
                name,
                str(count),
                desc,
                downloads_str
            )
            
        console.print(table)


@app.command()
def lookup():
    """Placeholder for future lookup command."""
    typer.echo("Lookup command - to be implemented")

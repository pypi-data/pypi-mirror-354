#!/usr/bin/env python3
"""
Proof of Concept: Dependency Explorer for good-dev

This demonstrates the core functionality of the proposed dependency explorer.
Run this script in a Python environment to see how it would work.
"""

import ast
import importlib.metadata
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import subprocess
import pkg_resources


class DependencyExplorer:
    """Core dependency exploration functionality"""
    
    def __init__(self, project_path: Path = Path.cwd()):
        self.project_path = project_path
        self._dependency_cache = {}
        
    def get_installed_packages(self) -> Dict[str, str]:
        """Get all installed packages with versions"""
        return {
            dist.metadata['Name']: dist.version 
            for dist in importlib.metadata.distributions()
        }
    
    def get_package_dependencies(self, package_name: str) -> Dict[str, List[str]]:
        """Get direct dependencies of a package"""
        try:
            dist = importlib.metadata.distribution(package_name)
            deps = []
            if dist.requires:
                for req in dist.requires:
                    # Parse requirement string
                    deps.append(str(req).split(';')[0].strip())
            return {package_name: deps}
        except importlib.metadata.PackageNotFoundError:
            return {package_name: []}
    
    def build_dependency_tree(self, package_name: str, max_depth: int = 3, 
                            _current_depth: int = 0, _seen: Optional[Set[str]] = None) -> Dict:
        """Build a recursive dependency tree"""
        if _seen is None:
            _seen = set()
            
        if package_name in _seen or _current_depth > max_depth:
            return {"name": package_name, "circular": True}
            
        _seen.add(package_name)
        
        deps = self.get_package_dependencies(package_name)
        children = []
        
        for dep_list in deps.values():
            for dep in dep_list:
                # Extract package name from requirement
                dep_name = dep.split('[')[0].split('<')[0].split('>')[0].split('=')[0].strip()
                if dep_name:
                    child = self.build_dependency_tree(
                        dep_name, max_depth, _current_depth + 1, _seen
                    )
                    children.append(child)
        
        return {
            "name": package_name,
            "version": self.get_installed_packages().get(package_name, "unknown"),
            "children": children
        }
    
    def search_in_package_code(self, package_name: str, pattern: str) -> List[Dict]:
        """Search for pattern in package source code"""
        results = []
        try:
            dist = importlib.metadata.distribution(package_name)
            if dist.files:
                for file in dist.files:
                    if file.suffix == '.py':
                        try:
                            # Get the file path
                            file_path = Path(dist.locate_file(file))
                            content = file_path.read_text(encoding='utf-8', errors='ignore')
                            
                            # Simple line-by-line search
                            for line_no, line in enumerate(content.splitlines(), 1):
                                if pattern.lower() in line.lower():
                                    results.append({
                                        "package": package_name,
                                        "file": str(file),
                                        "line": line_no,
                                        "content": line.strip(),
                                        "context": self._get_context(content.splitlines(), line_no - 1)
                                    })
                        except Exception:
                            pass
        except Exception:
            pass
        return results[:10]  # Limit results for demo
    
    def _get_context(self, lines: List[str], line_idx: int, context_size: int = 2) -> str:
        """Get lines around a match for context"""
        start = max(0, line_idx - context_size)
        end = min(len(lines), line_idx + context_size + 1)
        return '\n'.join(lines[start:end])
    
    def find_package_apis(self, package_name: str) -> List[Dict]:
        """Find public APIs exported by a package"""
        apis = []
        try:
            module = importlib.import_module(package_name)
            
            for name in dir(module):
                if not name.startswith('_'):  # Public API
                    obj = getattr(module, name)
                    api_info = {
                        "name": name,
                        "type": type(obj).__name__,
                        "module": package_name,
                        "doc": inspect.getdoc(obj) if hasattr(obj, '__doc__') else None
                    }
                    
                    # Add signature for callables
                    if callable(obj):
                        try:
                            import inspect
                            api_info["signature"] = str(inspect.signature(obj))
                        except:
                            api_info["signature"] = None
                            
                    apis.append(api_info)
        except ImportError:
            pass
            
        return apis[:20]  # Limit for demo
    
    def analyze_project_dependencies(self) -> Dict:
        """Analyze the current project's dependencies"""
        # Try to read from pyproject.toml or requirements.txt
        pyproject_path = self.project_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomllib
                with open(pyproject_path, 'rb') as f:
                    data = tomllib.load(f)
                    
                deps = []
                if 'project' in data and 'dependencies' in data['project']:
                    deps = data['project']['dependencies']
                elif 'tool' in data and 'poetry' in data['tool'] and 'dependencies' in data['tool']['poetry']:
                    deps = list(data['tool']['poetry']['dependencies'].keys())
                    
                return {"source": "pyproject.toml", "dependencies": deps}
            except:
                pass
                
        return {"source": "none", "dependencies": []}


def demo():
    """Run a demonstration of the dependency explorer"""
    explorer = DependencyExplorer()
    
    print("🔍 Dependency Explorer - Proof of Concept\n")
    
    # Demo 1: Show installed packages
    print("1. Sample of installed packages:")
    packages = explorer.get_installed_packages()
    for i, (name, version) in enumerate(list(packages.items())[:5]):
        print(f"   - {name} ({version})")
    print(f"   ... and {len(packages) - 5} more\n")
    
    # Demo 2: Show dependency tree for a common package
    print("2. Dependency tree for 'requests' (if installed):")
    if 'requests' in packages:
        tree = explorer.build_dependency_tree('requests', max_depth=2)
        print_tree(tree, indent="   ")
    else:
        print("   'requests' not installed - install it to see demo\n")
    
    # Demo 3: Search for functionality
    print("\n3. Search for 'json' in installed packages:")
    search_packages = ['requests', 'urllib3', 'setuptools']
    for pkg in search_packages:
        if pkg in packages:
            results = explorer.search_in_package_code(pkg, 'json')
            if results:
                print(f"   Found in {pkg}:")
                for r in results[:2]:  # Show first 2 results
                    print(f"     - {r['file']}:{r['line']} - {r['content'][:60]}...")
                break
    
    # Demo 4: Show how this would integrate with Claude Code
    print("\n4. Example MCP-style output for Claude Code:")
    if 'requests' in packages:
        apis = explorer.find_package_apis('requests')
        mcp_response = {
            "tool": "find_functionality",
            "query": "http client",
            "results": [
                {
                    "package": "requests",
                    "confidence": 0.95,
                    "apis": [api['name'] for api in apis[:5]],
                    "description": "Popular HTTP client library already in your dependencies"
                }
            ]
        }
        print(f"   {json.dumps(mcp_response, indent=2)}")


def print_tree(node: Dict, indent: str = "", is_last: bool = True):
    """Pretty print a dependency tree"""
    marker = "└── " if is_last else "├── "
    print(f"{indent}{marker}{node['name']} ({node.get('version', 'unknown')})")
    
    if 'circular' in node and node['circular']:
        return
        
    children = node.get('children', [])
    for i, child in enumerate(children):
        is_last_child = i == len(children) - 1
        extension = "    " if is_last else "│   "
        print_tree(child, indent + extension, is_last_child)


if __name__ == "__main__":
    import inspect  # Import here to use in find_package_apis
    demo()
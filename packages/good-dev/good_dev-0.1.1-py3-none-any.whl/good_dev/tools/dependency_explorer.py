"""
Dependency explorer for discovering functionality within existing dependencies.

This module provides tools to:
- Build and visualize dependency trees
- Search for functionality across installed packages
- Discover package communities based on shared dependencies
- Find APIs and code patterns in the dependency graph
"""

import ast
import importlib.metadata
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from loguru import logger


class DependencyExplorer:
    """Core dependency exploration functionality."""
    
    def __init__(self, project_path: Optional[Path] = None):
        """Initialize the dependency explorer.
        
        Args:
            project_path: Path to the project root. Defaults to current directory.
        """
        self.project_path = project_path or Path.cwd()
        self._metadata_cache: Dict[str, Any] = {}
        self._dependency_cache: Dict[str, List[str]] = {}
        
    def get_installed_packages(self) -> Dict[str, str]:
        """Get all installed packages with their versions.
        
        Returns:
            Dictionary mapping package names to versions.
        """
        packages = {}
        for dist in importlib.metadata.distributions():
            name = dist.metadata.get('Name', '')
            version = dist.version
            if name:
                packages[name.lower()] = version
        return packages
    
    def get_package_metadata(self, package_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific package.
        
        Args:
            package_name: Name of the package.
            
        Returns:
            Package metadata or None if not found.
        """
        if package_name in self._metadata_cache:
            return self._metadata_cache[package_name]
            
        try:
            dist = importlib.metadata.distribution(package_name)
            metadata = {
                'name': dist.metadata.get('Name', package_name),
                'version': dist.version,
                'summary': dist.metadata.get('Summary', ''),
                'home_page': dist.metadata.get('Home-Page', ''),
                'author': dist.metadata.get('Author', ''),
                'license': dist.metadata.get('License', ''),
                'requires_python': dist.metadata.get('Requires-Python', ''),
                'classifiers': dist.metadata.get_all('Classifier', []),
                'files': [str(f) for f in (dist.files or [])]
            }
            self._metadata_cache[package_name] = metadata
            return metadata
        except importlib.metadata.PackageNotFoundError:
            logger.warning(f"Package {package_name} not found")
            return None
    
    def get_package_dependencies(self, package_name: str) -> List[str]:
        """Get direct dependencies of a package.
        
        Args:
            package_name: Name of the package.
            
        Returns:
            List of dependency names (without version specifiers).
        """
        cache_key = package_name.lower()
        if cache_key in self._dependency_cache:
            return self._dependency_cache[cache_key]
            
        dependencies = []
        try:
            dist = importlib.metadata.distribution(package_name)
            if dist.requires:
                for req in dist.requires:
                    # Parse requirement string to get package name
                    # Handle cases like "package[extra]>=1.0,<2.0"
                    dep_name = re.split(r'[<>=\[]', req)[0].strip()
                    if dep_name and ';' not in dep_name:  # Skip conditional deps for now
                        dependencies.append(dep_name.lower())
            
            self._dependency_cache[cache_key] = dependencies
        except importlib.metadata.PackageNotFoundError:
            logger.warning(f"Package {package_name} not found")
            
        return dependencies
    
    def build_dependency_tree(
        self, 
        package_name: str, 
        max_depth: int = 3,
        include_versions: bool = True,
        _current_depth: int = 0,
        _seen: Optional[Set[str]] = None
    ) -> Dict[str, Any]:
        """Build a recursive dependency tree for a package.
        
        Args:
            package_name: Name of the package.
            max_depth: Maximum depth to traverse.
            include_versions: Whether to include version information.
            _current_depth: Current recursion depth (internal use).
            _seen: Set of seen packages to detect cycles (internal use).
            
        Returns:
            Dictionary representing the dependency tree.
        """
        if _seen is None:
            _seen = set()
            
        normalized_name = package_name.lower()
        
        # Handle circular dependencies
        if normalized_name in _seen:
            return {
                'name': package_name,
                'circular': True
            }
            
        if _current_depth >= max_depth:
            return {
                'name': package_name,
                'truncated': True
            }
            
        _seen.add(normalized_name)
        
        # Build tree node
        node: Dict[str, Any] = {'name': package_name}
        
        if include_versions:
            packages = self.get_installed_packages()
            if normalized_name in packages:
                node['version'] = packages[normalized_name]
        
        # Get dependencies
        dependencies = self.get_package_dependencies(package_name)
        if dependencies:
            node['dependencies'] = []
            for dep in dependencies:
                child = self.build_dependency_tree(
                    dep,
                    max_depth,
                    include_versions,
                    _current_depth + 1,
                    _seen.copy()  # Use copy to allow same package at different paths
                )
                node['dependencies'].append(child)
                
        return node
    
    def search_package_code(
        self, 
        pattern: str,
        package_name: Optional[str] = None,
        search_type: str = 'all',
        case_sensitive: bool = False,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """Search for patterns in package source code.
        
        Args:
            pattern: Search pattern (regex).
            package_name: Specific package to search in. None searches all.
            search_type: Type of search ('all', 'function', 'class', 'import').
            case_sensitive: Whether search is case sensitive.
            max_results: Maximum number of results to return.
            
        Returns:
            List of search results.
        """
        results = []
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(pattern, flags)
        
        # Determine packages to search
        if package_name:
            packages = [package_name] if package_name in self.get_installed_packages() else []
        else:
            packages = list(self.get_installed_packages().keys())
            
        for pkg in packages:
            if len(results) >= max_results:
                break
                
            try:
                dist = importlib.metadata.distribution(pkg)
                if not dist.files:
                    continue
                    
                for file in dist.files:
                    if len(results) >= max_results:
                        break
                        
                    if file.suffix != '.py':
                        continue
                        
                    try:
                        file_path = Path(dist.locate_file(file))
                        if not file_path.exists():
                            continue
                            
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        
                        if search_type == 'all':
                            # Simple line search
                            for line_no, line in enumerate(content.splitlines(), 1):
                                if regex.search(line):
                                    results.append({
                                        'package': pkg,
                                        'file': str(file),
                                        'line': line_no,
                                        'content': line.strip(),
                                        'type': 'text'
                                    })
                        else:
                            # AST-based search
                            results.extend(self._search_ast(
                                content, file_path, pkg, str(file), 
                                regex, search_type
                            ))
                            
                    except Exception as e:
                        logger.debug(f"Error searching {file}: {e}")
                        
            except Exception as e:
                logger.debug(f"Error searching package {pkg}: {e}")
                
        return results[:max_results]
    
    def _search_ast(
        self,
        content: str,
        file_path: Path,
        package: str,
        file_str: str,
        regex: re.Pattern,
        search_type: str
    ) -> List[Dict[str, Any]]:
        """Search using AST parsing for specific code constructs.
        
        Args:
            content: File content.
            file_path: Path to the file.
            package: Package name.
            file_str: File path as string.
            regex: Compiled regex pattern.
            search_type: Type of search.
            
        Returns:
            List of search results.
        """
        results = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                match = False
                node_info = None
                
                if search_type == 'function' and isinstance(node, ast.FunctionDef):
                    if regex.search(node.name):
                        match = True
                        node_info = {
                            'name': node.name,
                            'signature': self._get_function_signature(node),
                            'docstring': ast.get_docstring(node)
                        }
                elif search_type == 'class' and isinstance(node, ast.ClassDef):
                    if regex.search(node.name):
                        match = True
                        node_info = {
                            'name': node.name,
                            'bases': [self._ast_to_str(base) for base in node.bases],
                            'docstring': ast.get_docstring(node)
                        }
                elif search_type == 'import' and isinstance(node, (ast.Import, ast.ImportFrom)):
                    import_str = self._get_import_string(node)
                    if regex.search(import_str):
                        match = True
                        node_info = {'import': import_str}
                        
                if match and hasattr(node, 'lineno'):
                    results.append({
                        'package': package,
                        'file': file_str,
                        'line': node.lineno,
                        'type': search_type,
                        'info': node_info
                    })
                    
        except SyntaxError:
            logger.debug(f"Syntax error parsing {file_path}")
            
        return results
    
    def _get_function_signature(self, node: ast.FunctionDef) -> str:
        """Extract function signature from AST node."""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        return f"{node.name}({', '.join(args)})"
    
    def _ast_to_str(self, node: ast.AST) -> str:
        """Convert AST node to string representation."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._ast_to_str(node.value)}.{node.attr}"
        else:
            return str(node)
    
    def _get_import_string(self, node: ast.AST) -> str:
        """Get import statement as string."""
        if isinstance(node, ast.Import):
            return ', '.join(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names = ', '.join(alias.name for alias in node.names)
            return f"from {node.module} import {names}"
        return ""
    
    def find_package_apis(
        self, 
        package_name: str,
        include_private: bool = False,
        filter_pattern: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Find APIs exported by a package.
        
        Args:
            package_name: Name of the package.
            include_private: Whether to include private APIs (starting with _).
            filter_pattern: Optional regex pattern to filter API names.
            
        Returns:
            List of API information.
        """
        apis = []
        
        try:
            # Try to import the module
            module = importlib.import_module(package_name)
            
            for name in dir(module):
                if not include_private and name.startswith('_'):
                    continue
                    
                if filter_pattern and not re.search(filter_pattern, name, re.IGNORECASE):
                    continue
                    
                try:
                    obj = getattr(module, name)
                    api_info = {
                        'name': name,
                        'type': type(obj).__name__,
                        'module': package_name,
                        'qualname': f"{package_name}.{name}"
                    }
                    
                    # Add documentation
                    if hasattr(obj, '__doc__') and obj.__doc__:
                        api_info['doc'] = obj.__doc__.strip()
                        
                    # Add signature for callables
                    if callable(obj):
                        try:
                            import inspect
                            sig = inspect.signature(obj)
                            api_info['signature'] = str(sig)
                        except (ValueError, TypeError):
                            pass
                            
                    apis.append(api_info)
                    
                except Exception as e:
                    logger.debug(f"Error inspecting {name}: {e}")
                    
        except ImportError as e:
            logger.warning(f"Cannot import package {package_name}: {e}")
            
        return apis
    
    def get_project_dependencies(self) -> Dict[str, Any]:
        """Get dependencies defined in the current project.
        
        Returns:
            Dictionary with project dependency information.
        """
        # Try pyproject.toml first
        pyproject_path = self.project_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                import tomllib
                with open(pyproject_path, 'rb') as f:
                    data = tomllib.load(f)
                    
                dependencies = []
                optional_dependencies = {}
                
                # Handle different pyproject.toml formats
                if 'project' in data:
                    # PEP 621 format
                    dependencies = data['project'].get('dependencies', [])
                    optional_dependencies = data['project'].get('optional-dependencies', {})
                elif 'tool' in data and 'poetry' in data['tool']:
                    # Poetry format
                    deps = data['tool']['poetry'].get('dependencies', {})
                    dependencies = [f"{k}{v}" if isinstance(v, str) and v.startswith(('>', '<', '=')) else k 
                                  for k, v in deps.items() if k != 'python']
                    
                return {
                    'source': 'pyproject.toml',
                    'dependencies': dependencies,
                    'optional_dependencies': optional_dependencies
                }
            except Exception as e:
                logger.error(f"Error reading pyproject.toml: {e}")
                
        # Try requirements.txt
        requirements_path = self.project_path / "requirements.txt"
        if requirements_path.exists():
            try:
                dependencies = []
                with open(requirements_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            dependencies.append(line)
                            
                return {
                    'source': 'requirements.txt',
                    'dependencies': dependencies,
                    'optional_dependencies': {}
                }
            except Exception as e:
                logger.error(f"Error reading requirements.txt: {e}")
                
        return {
            'source': 'none',
            'dependencies': [],
            'optional_dependencies': {}
        }
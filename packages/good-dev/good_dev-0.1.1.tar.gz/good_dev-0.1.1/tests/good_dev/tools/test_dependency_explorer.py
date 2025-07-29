"""Tests for the dependency explorer functionality."""

import json
import re
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest
import importlib.metadata

from good_dev.tools.dependency_explorer import DependencyExplorer


@pytest.fixture
def explorer():
    """Create a DependencyExplorer instance for testing."""
    return DependencyExplorer(Path("/tmp/test_project"))


@pytest.fixture
def mock_distributions():
    """Mock importlib.metadata.distributions."""
    mock_dist1 = Mock()
    mock_dist1.metadata = {'Name': 'requests', 'Summary': 'HTTP library'}
    mock_dist1.version = '2.31.0'
    mock_dist1.requires = ['charset-normalizer>=2,<4', 'urllib3>=1.21.1,<3']
    
    mock_dist2 = Mock()
    mock_dist2.metadata = {'Name': 'urllib3', 'Summary': 'HTTP client'}
    mock_dist2.version = '2.0.7'
    mock_dist2.requires = []
    
    return [mock_dist1, mock_dist2]


class TestDependencyExplorer:
    """Test the DependencyExplorer class."""
    
    def test_get_installed_packages(self, explorer, mock_distributions):
        """Test getting installed packages."""
        with patch('importlib.metadata.distributions', return_value=mock_distributions):
            packages = explorer.get_installed_packages()
            
            assert 'requests' in packages
            assert packages['requests'] == '2.31.0'
            assert 'urllib3' in packages
            assert packages['urllib3'] == '2.0.7'
    
    def test_get_package_dependencies(self, explorer):
        """Test extracting package dependencies."""
        # Test with mock distribution
        mock_dist = Mock()
        mock_dist.requires = [
            'charset-normalizer>=2,<4',
            'urllib3>=1.21.1,<3',
            'certifi>=2017.4.17',
            'idna>=2.5,<4;python_version<"3.8"'  # Conditional dependency
        ]
        
        with patch('importlib.metadata.distribution', return_value=mock_dist):
            deps = explorer.get_package_dependencies('requests')
            
            assert 'charset-normalizer' in deps
            assert 'urllib3' in deps
            assert 'certifi' in deps
            # Conditional dependencies should be skipped for now
            assert 'idna' not in deps
    
    def test_build_dependency_tree(self, explorer):
        """Test building dependency tree with circular dependency handling."""
        # Mock the dependency structure
        def mock_get_deps(package):
            deps_map = {
                'package-a': ['package-b', 'package-c'],
                'package-b': ['package-d'],
                'package-c': ['package-d'],
                'package-d': ['package-a']  # Circular dependency
            }
            return deps_map.get(package.lower(), [])
        
        explorer.get_package_dependencies = mock_get_deps
        explorer.get_installed_packages = lambda: {
            'package-a': '1.0.0',
            'package-b': '2.0.0',
            'package-c': '3.0.0',
            'package-d': '4.0.0'
        }
        
        tree = explorer.build_dependency_tree('package-a', max_depth=5)
        
        assert tree['name'] == 'package-a'
        assert tree['version'] == '1.0.0'
        assert len(tree['dependencies']) == 2
        
        # Check that circular dependency is marked
        package_d = tree['dependencies'][0]['dependencies'][0]
        assert package_d['name'] == 'package-d'
        assert 'dependencies' in package_d
        # The circular reference back to package-a should be marked
        circular_ref = package_d['dependencies'][0]
        assert circular_ref['name'] == 'package-a'
        assert circular_ref.get('circular') is True
    
    def test_build_dependency_tree_max_depth(self, explorer):
        """Test that max_depth is respected."""
        def mock_get_deps(package):
            # Create a deep chain
            return [f'dep-{int(package[-1]) + 1}'] if package.startswith('dep-') and int(package[-1]) < 9 else []
        
        explorer.get_package_dependencies = mock_get_deps
        explorer.get_installed_packages = lambda: {f'dep-{i}': f'{i}.0.0' for i in range(10)}
        
        tree = explorer.build_dependency_tree('dep-1', max_depth=3)
        
        # Count depth
        def count_depth(node, current=0):
            if 'truncated' in node and node['truncated']:
                return current
            if 'dependencies' not in node:
                return current
            return max([count_depth(dep, current + 1) for dep in node['dependencies']] + [current])
        
        depth = count_depth(tree)
        assert depth == 3  # Should stop at max_depth
    
    def test_search_package_code_ast(self, explorer):
        """Test AST-based code search."""
        # Create a mock Python file content
        mock_content = '''
def calculate_total(items):
    """Calculate the total of items."""
    return sum(items)

class Calculator:
    """A simple calculator class."""
    def add(self, a, b):
        return a + b

import json
from typing import List
'''
        
        results = explorer._search_ast(
            mock_content,
            Path('/fake/path.py'),
            'test-package',
            'module.py',
            re.compile(r'calc', re.IGNORECASE),
            'function'
        )
        
        assert len(results) == 1
        assert results[0]['info']['name'] == 'calculate_total'
        assert results[0]['line'] == 2
        
        # Test class search
        results = explorer._search_ast(
            mock_content,
            Path('/fake/path.py'),
            'test-package',
            'module.py',
            re.compile(r'Calc', re.IGNORECASE),
            'class'
        )
        
        assert len(results) == 1
        assert results[0]['info']['name'] == 'Calculator'
        assert results[0]['line'] == 6
    
    def test_clean_dependencies_list(self):
        """Test the clean_dependencies_list function from wheelodex."""
        from good_dev.tools.wheelodex._api import clean_dependencies_list
        
        deps = [
            'requests>=2.0.0',
            'django<4.0',
            'pytest~=7.0',
            'numpy[extra]>=1.20',
            'flask==2.0.0;python_version>="3.7"'
        ]
        
        cleaned = clean_dependencies_list(deps)
        
        assert 'requests' in cleaned
        assert 'django' in cleaned
        assert 'pytest' in cleaned
        assert 'numpy' in cleaned
        assert 'flask' in cleaned
        assert len(cleaned) == 5
        
        # Version specifiers should be removed
        for dep in cleaned:
            assert '<' not in dep
            assert '>' not in dep
            assert '=' not in dep
            assert '[' not in dep
    
    def test_get_project_dependencies_pyproject(self, explorer, tmp_path):
        """Test reading dependencies from pyproject.toml."""
        explorer.project_path = tmp_path
        
        # Create a test pyproject.toml
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text('''
[project]
dependencies = [
    "requests>=2.28.0",
    "pydantic>=2.0.0",
    "typer>=0.9.0"
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=23.0"]
test = ["pytest-cov>=4.0"]
''')
        
        result = explorer.get_project_dependencies()
        
        assert result['source'] == 'pyproject.toml'
        assert len(result['dependencies']) == 3
        assert 'requests>=2.28.0' in result['dependencies']
        assert 'pydantic>=2.0.0' in result['dependencies']
        assert 'dev' in result['optional_dependencies']
        assert 'pytest>=7.0' in result['optional_dependencies']['dev']
    
    def test_get_project_dependencies_requirements(self, explorer, tmp_path):
        """Test reading dependencies from requirements.txt."""
        explorer.project_path = tmp_path
        
        # Create a test requirements.txt
        requirements = tmp_path / "requirements.txt"
        requirements.write_text('''
# Core dependencies
requests>=2.28.0
pydantic>=2.0.0

# CLI
typer>=0.9.0

# Testing - commented out
# pytest>=7.0
''')
        
        result = explorer.get_project_dependencies()
        
        assert result['source'] == 'requirements.txt'
        assert len(result['dependencies']) == 3
        assert 'requests>=2.28.0' in result['dependencies']
        assert 'typer>=0.9.0' in result['dependencies']
        # Comments should be ignored
        assert not any('pytest' in dep for dep in result['dependencies'])
    
    def test_find_package_apis_filtering(self, explorer):
        """Test API discovery with filtering."""
        # Create a mock module
        mock_module = MagicMock()
        mock_module.public_func = lambda: None
        mock_module._private_func = lambda: None
        mock_module.CalculatorClass = type('CalculatorClass', (), {})
        mock_module.CONSTANT = 42
        
        with patch('importlib.import_module', return_value=mock_module):
            # Test without private APIs
            apis = explorer.find_package_apis('test_package', include_private=False)
            api_names = [api['name'] for api in apis]
            
            assert 'public_func' in api_names
            assert '_private_func' not in api_names
            assert 'CalculatorClass' in api_names
            assert 'CONSTANT' in api_names
            
            # Test with filter pattern
            apis = explorer.find_package_apis('test_package', filter_pattern=r'calc', include_private=False)
            api_names = [api['name'] for api in apis]
            
            assert 'CalculatorClass' in api_names
            assert 'public_func' not in api_names
            assert 'CONSTANT' not in api_names
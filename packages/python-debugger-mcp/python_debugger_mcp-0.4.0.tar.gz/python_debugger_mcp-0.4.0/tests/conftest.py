"""Pytest configuration and shared fixtures for python-debugger-mcp tests."""

import os
import tempfile
import pytest
from unittest.mock import Mock, patch
from pathlib import Path


@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for test files."""
    return tmp_path


@pytest.fixture
def sample_python_file(temp_dir):
    """Create a sample Python file for testing."""
    test_file = temp_dir / "test_script.py"
    test_file.write_text("""
def add_numbers(a, b):
    '''Add two numbers together.'''
    result = a + b
    return result

def multiply_numbers(a, b):
    '''Multiply two numbers together.'''
    result = a * b
    return result

if __name__ == "__main__":
    x = 5
    y = 10
    sum_result = add_numbers(x, y)
    multiply_result = multiply_numbers(x, y)
    print(f"Sum: {sum_result}, Product: {multiply_result}")
""")
    return str(test_file)


@pytest.fixture
def sample_project_structure(temp_dir):
    """Create a sample project structure with pyproject.toml."""
    # Create pyproject.toml
    pyproject_file = temp_dir / "pyproject.toml"
    pyproject_file.write_text("""
[project]
name = "test-project"
version = "0.1.0"
dependencies = []
""")
    
    # Create a source directory
    src_dir = temp_dir / "src"
    src_dir.mkdir()
    
    # Create a test file in src
    test_file = src_dir / "main.py"
    test_file.write_text("""
def main():
    print("Hello, World!")
    return 42

if __name__ == "__main__":
    result = main()
    print(f"Result: {result}")
""")
    
    return {
        "root": str(temp_dir),
        "pyproject": str(pyproject_file),
        "test_file": str(test_file),
    }


@pytest.fixture
def mock_subprocess():
    """Mock subprocess operations."""
    with patch('subprocess.Popen') as mock_popen:
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.stdout = Mock()
        mock_process.communicate.return_value = (b"", b"")
        mock_popen.return_value = mock_process
        yield mock_process


@pytest.fixture
def reset_global_state():
    """Reset global state before and after each test."""
    # Store original values
    from src.python_debugger_mcp.main import (
        pdb_process, pdb_running, current_file, current_project_root,
        current_args, current_use_pytest, breakpoints, output_thread
    )
    
    original_state = {
        'pdb_process': pdb_process,
        'pdb_running': pdb_running,
        'current_file': current_file,
        'current_project_root': current_project_root,
        'current_args': current_args,
        'current_use_pytest': current_use_pytest,
        'breakpoints': breakpoints.copy(),
        'output_thread': output_thread,
    }
    
    yield
    
    # Reset global variables
    import src.python_debugger_mcp.main as main_module
    main_module.pdb_process = None
    main_module.pdb_running = False
    main_module.current_file = None
    main_module.current_project_root = None
    main_module.current_args = ""
    main_module.current_use_pytest = False
    main_module.breakpoints = {}
    main_module.output_thread = None


@pytest.fixture
def mock_environment_detection():
    """Mock environment detection functions."""
    with patch('shutil.which') as mock_which, \
         patch('os.path.exists') as mock_exists:
        
        def mock_which_func(cmd):
            if cmd == "uv":
                return "/usr/local/bin/uv"
            elif cmd == "python":
                return "/usr/bin/python"
            elif cmd == "pytest":
                return "/usr/bin/pytest"
            return None
        
        mock_which.side_effect = mock_which_func
        mock_exists.return_value = True
        
        yield {
            'which': mock_which,
            'exists': mock_exists,
        } 
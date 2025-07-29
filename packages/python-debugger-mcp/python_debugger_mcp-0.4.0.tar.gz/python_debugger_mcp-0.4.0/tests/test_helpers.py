"""Unit tests for helper functions in python-debugger-mcp."""

import os
import pytest
from unittest.mock import patch, Mock, mock_open
from pathlib import Path

from src.python_debugger_mcp.main import (
    find_project_root,
    find_venv_details,
    sanitize_arguments,
    get_pdb_output,
)


class TestFindProjectRoot:
    """Tests for find_project_root function."""
    
    def test_find_project_root_with_pyproject_toml(self, temp_dir):
        """Test finding project root with pyproject.toml."""
        # Create a nested directory structure
        subdir = temp_dir / "src" / "package"
        subdir.mkdir(parents=True)
        
        # Create pyproject.toml in root
        (temp_dir / "pyproject.toml").touch()
        
        # Test from subdirectory
        result = find_project_root(str(subdir))
        assert result == str(temp_dir)
    
    def test_find_project_root_with_git(self, temp_dir):
        """Test finding project root with .git directory."""
        subdir = temp_dir / "src"
        subdir.mkdir()
        
        # Create .git directory
        (temp_dir / ".git").mkdir()
        
        result = find_project_root(str(subdir))
        assert result == str(temp_dir)
    
    def test_find_project_root_multiple_indicators(self, temp_dir):
        """Test with multiple project indicators."""
        subdir = temp_dir / "src" / "deep"
        subdir.mkdir(parents=True)
        
        # Create multiple indicators
        (temp_dir / "pyproject.toml").touch()
        (temp_dir / ".git").mkdir()
        (temp_dir / "setup.py").touch()
        
        result = find_project_root(str(subdir))
        assert result == str(temp_dir)
    
    def test_find_project_root_no_indicators(self, temp_dir):
        """Test fallback when no indicators found."""
        subdir = temp_dir / "src"
        subdir.mkdir()
        
        result = find_project_root(str(subdir))
        assert result == str(subdir)
    
    def test_find_project_root_from_file(self, temp_dir):
        """Test finding project root when starting from a file path."""
        subdir = temp_dir / "src"
        subdir.mkdir()
        test_file = subdir / "test.py"
        test_file.touch()
        
        (temp_dir / "pyproject.toml").touch()
        
        result = find_project_root(str(test_file))
        assert result == str(temp_dir)


class TestFindVenvDetails:
    """Tests for find_venv_details function."""
    
    @patch.dict(os.environ, {'VIRTUAL_ENV': '/path/to/venv'})
    @patch('os.path.isdir')
    @patch('os.path.exists')
    def test_find_active_virtual_env(self, mock_exists, mock_isdir):
        """Test detection of active virtual environment."""
        mock_isdir.return_value = True
        mock_exists.return_value = True
        
        python_exe, bin_dir = find_venv_details("/some/project")
        
        assert python_exe == "/path/to/venv/bin/python"
        assert bin_dir == "/path/to/venv/bin"
    
    @patch.dict(os.environ, {'CONDA_PREFIX': '/path/to/conda'})
    @patch('os.path.isdir')
    @patch('os.path.exists')
    def test_find_conda_environment(self, mock_exists, mock_isdir):
        """Test detection of conda environment."""
        mock_isdir.return_value = True
        mock_exists.return_value = True
        
        # Clear VIRTUAL_ENV if it exists
        with patch.dict(os.environ, {}, clear=False):
            if 'VIRTUAL_ENV' in os.environ:
                del os.environ['VIRTUAL_ENV']
            
            python_exe, bin_dir = find_venv_details("/some/project")
            
            assert python_exe == "/path/to/conda/bin/python"
            assert bin_dir == "/path/to/conda/bin"
    
    def test_find_local_venv(self, temp_dir):
        """Test finding local virtual environment directories."""
        # Create a .venv directory
        venv_dir = temp_dir / ".venv"
        venv_dir.mkdir()
        bin_dir = venv_dir / "bin"
        bin_dir.mkdir()
        python_exe = bin_dir / "python"
        python_exe.touch()
        
        # Clear environment variables
        with patch.dict(os.environ, {}, clear=True):
            result = find_venv_details(str(temp_dir))
            
            assert result is not None
            python_path, bin_path = result
            assert python_path == str(python_exe)
            assert bin_path == str(bin_dir)
    
    def test_no_venv_found(self, temp_dir):
        """Test when no virtual environment is found."""
        with patch.dict(os.environ, {}, clear=True):
            result = find_venv_details(str(temp_dir))
            assert result == (None, None)


class TestSanitizeArguments:
    """Tests for sanitize_arguments function."""
    
    def test_sanitize_simple_arguments(self):
        """Test sanitizing simple arguments."""
        result = sanitize_arguments("arg1 arg2 arg3")
        assert result == ["arg1", "arg2", "arg3"]
    
    def test_sanitize_quoted_arguments(self):
        """Test sanitizing quoted arguments."""
        result = sanitize_arguments('arg1 "quoted arg" arg3')
        assert result == ["arg1", "quoted arg", "arg3"]
    
    def test_sanitize_mixed_quotes(self):
        """Test sanitizing arguments with mixed quotes."""
        result = sanitize_arguments("""arg1 'single quoted' "double quoted" """)
        assert result == ["arg1", "single quoted", "double quoted"]
    
    def test_sanitize_empty_string(self):
        """Test sanitizing empty string."""
        result = sanitize_arguments("")
        assert result == []
    
    def test_sanitize_whitespace_only(self):
        """Test sanitizing whitespace-only string."""
        result = sanitize_arguments("   \t\n  ")
        assert result == []
    
    def test_sanitize_special_characters(self):
        """Test sanitizing arguments with special characters."""
        result = sanitize_arguments("--verbose --output=file.txt")
        assert result == ["--verbose", "--output=file.txt"]


class TestGetPdbOutput:
    """Tests for get_pdb_output function."""
    
    @patch('src.python_debugger_mcp.main.pdb_output_queue')
    @patch('time.monotonic')
    def test_get_pdb_output_with_data(self, mock_time, mock_queue):
        """Test getting PDB output with data in queue."""
        # Mock time to control timeout
        mock_time.side_effect = [0, 0.1, 0.2, 0.3]  # Simulate time progression
        
        # Mock queue with test data
        mock_queue.get.side_effect = [
            "Line 1",
            "Line 2", 
            "(Pdb) ",  # This should trigger the break
        ]
        mock_queue.empty = Mock(return_value=False)
        
        result = get_pdb_output(timeout=0.5)
        
        assert "Line 1" in result
        assert "Line 2" in result
        assert "(Pdb)" in result
    
    @patch('src.python_debugger_mcp.main.pdb_output_queue')
    @patch('time.monotonic')
    def test_get_pdb_output_timeout(self, mock_time, mock_queue):
        """Test get_pdb_output when timeout is reached."""
        # Mock time to simulate timeout
        mock_time.side_effect = [0, 0.6]  # Exceed timeout
        
        # Mock queue to raise Empty exception (timeout)
        from queue import Empty
        mock_queue.get.side_effect = Empty()
        
        result = get_pdb_output(timeout=0.5)
        
        assert result == ""  # Should return empty string on timeout
    
    @patch('src.python_debugger_mcp.main.pdb_output_queue')
    def test_get_pdb_output_empty_queue(self, mock_queue):
        """Test get_pdb_output with empty queue."""
        from queue import Empty
        mock_queue.get.side_effect = Empty()
        
        result = get_pdb_output(timeout=0.1)
        
        assert result == ""


@pytest.mark.unit
class TestPythonCompatibility:
    """Test Python version compatibility features."""
    
    def test_f_strings(self):
        """Test f-string functionality (Python 3.6+)."""
        name = "test"
        value = 42
        result = f"Name: {name}, Value: {value}"
        assert result == "Name: test, Value: 42"
    
    def test_pathlib(self, temp_dir):
        """Test pathlib functionality (Python 3.4+)."""
        path = Path(temp_dir) / "test.txt"
        path.write_text("test content")
        content = path.read_text()
        assert content == "test content"
    
    def test_subprocess_functionality(self):
        """Test subprocess functionality used in the module."""
        import subprocess
        import shlex
        
        # Test shlex.quote (used in the code)
        unsafe_arg = "file with spaces.py"
        quoted = shlex.quote(unsafe_arg)
        assert quoted == "'file with spaces.py'"
    
    def test_threading_functionality(self):
        """Test threading functionality used in the module."""
        import threading
        import queue
        import time
        
        test_queue = queue.Queue()
        
        def worker():
            test_queue.put("test_message")
        
        thread = threading.Thread(target=worker)
        thread.start()
        thread.join(timeout=1.0)
        
        assert not test_queue.empty()
        assert test_queue.get() == "test_message"
    
    def test_regex_functionality(self):
        """Test regex functionality used in the module."""
        import re
        
        text = "Breakpoint 1 at /path/to/file.py:42"
        match = re.search(r"Breakpoint (\d+) at", text)
        
        assert match is not None
        assert match.group(1) == "1" 
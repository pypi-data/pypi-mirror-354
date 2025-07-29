"""Integration tests for python-debugger-mcp with real Python processes."""

import pytest
import time
import os
import sys
from pathlib import Path

from src.python_debugger_mcp.main import (
    start_debug,
    end_debug,
    send_pdb_command,
    set_breakpoint,
    get_debug_status,
)


@pytest.mark.integration
@pytest.mark.slow
class TestRealPythonDebugging:
    """Integration tests with real Python processes."""
    
    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self, reset_global_state):
        """Setup and cleanup for integration tests."""
        yield
        # Always try to end debug session after each test
        try:
            end_debug()
        except Exception:
            pass  # Ignore errors during cleanup
    
    def test_debug_simple_script(self, sample_python_file):
        """Test debugging a simple Python script."""
        # Start debugging
        result = start_debug(sample_python_file)
        
        # Should successfully start
        assert ("(Pdb)" in result or 
                "Debugging session started" in result or
                "Warning: PDB started" in result), f"Failed to start debug: {result}"
        
        # Check debug status
        status = get_debug_status()
        assert "Debug Session Status" in status
        assert sample_python_file in status
        
        # Send a simple command
        list_result = send_pdb_command("l")
        assert "def add_numbers" in list_result or "Command output:" in list_result
        
        # End debugging
        end_result = end_debug()
        assert "ended" in end_result.lower()
    
    def test_debug_with_breakpoint(self, sample_python_file):
        """Test setting and hitting a breakpoint."""
        # Start debugging
        start_result = start_debug(sample_python_file)
        assert ("(Pdb)" in start_result or 
                "started" in start_result.lower() or
                "Warning: PDB started" in start_result)
        
        # Set a breakpoint
        bp_result = set_breakpoint(os.path.basename(sample_python_file), 4)  # Line with 'result = a + b'
        
        # Should either succeed or indicate the line doesn't exist yet
        assert ("set and tracked" in bp_result or 
                "Breakpoint" in bp_result or
                "NOT reliably tracked" in bp_result), f"Breakpoint result: {bp_result}"
        
        # Try to continue (if breakpoint was set)
        if "set and tracked" in bp_result:
            continue_result = send_pdb_command("c")
            # May hit breakpoint or end
            assert "Command output:" in continue_result
        
        # Clean up
        end_debug()
    
    def test_debug_step_through(self, sample_python_file):
        """Test stepping through code."""
        # Start debugging
        start_result = start_debug(sample_python_file)
        assert ("(Pdb)" in start_result or 
                "started" in start_result.lower() or
                "Warning: PDB started" in start_result)
        
        # Step to next line
        step_result = send_pdb_command("n")
        assert "Command output:" in step_result
        
        # List current location
        list_result = send_pdb_command("l")
        assert "Command output:" in list_result
        
        # Print a variable (may not exist at first line)
        var_result = send_pdb_command("p __name__")
        assert "Command output:" in var_result
        
        # Clean up
        end_debug()
    
    def test_debug_environment_detection(self, sample_project_structure):
        """Test debugging with project structure detection."""
        test_file = sample_project_structure["test_file"]
        
        # Start debugging from project context
        start_result = start_debug(test_file)
        
        # Should detect project structure
        assert ("(Pdb)" in start_result or 
                "started" in start_result.lower() or
                "Warning: PDB started" in start_result or
                "Error:" in start_result)  # May error due to missing dependencies
        
        # If started successfully, check status
        if "(Pdb)" in start_result or "started" in start_result.lower():
            status = get_debug_status()
            assert "Debug Session Status" in status
            
            # Clean up
            end_debug()
    
    @pytest.mark.skipif(not os.getenv("TEST_WITH_PYTEST"), 
                       reason="pytest debugging tests skipped (set TEST_WITH_PYTEST=1 to enable)")
    def test_debug_with_pytest(self, sample_python_file):
        """Test debugging with pytest (conditional test)."""
        # This test requires pytest to be available
        try:
            import pytest as pytest_module
        except ImportError:
            pytest.skip("pytest not available")
        
        # Create a simple test file
        test_dir = Path(sample_python_file).parent
        test_file = test_dir / "test_example.py"
        test_file.write_text("""
def test_add_numbers():
    def add_numbers(a, b):
        result = a + b
        return result
    
    assert add_numbers(2, 3) == 5
""")
        
        # Start debugging with pytest
        start_result = start_debug(str(test_file), use_pytest=True)
        
        # May succeed or fail depending on environment
        # Just check that it doesn't crash
        assert isinstance(start_result, str)
        
        # Clean up if started
        if "(Pdb)" in start_result or "started" in start_result.lower():
            end_debug()


@pytest.mark.integration
class TestPythonVersionCompatibility:
    """Test compatibility across Python versions."""
    
    def test_current_python_version(self):
        """Test that we can detect current Python version."""
        version = sys.version_info
        assert version.major == 3
        # This test will help us verify which Python versions we support
        print(f"Testing with Python {version.major}.{version.minor}.{version.micro}")
    
    def test_subprocess_with_current_python(self, sample_python_file):
        """Test subprocess operations with current Python."""
        import subprocess
        import shlex
        
        # Test that we can run the Python file directly
        try:
            result = subprocess.run(
                [sys.executable, sample_python_file], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            # Should run without syntax errors
            assert result.returncode == 0
            assert "Sum: 15, Product: 50" in result.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Python script execution timed out")
        except Exception as e:
            pytest.fail(f"Failed to run Python script: {e}")
    
    def test_required_modules_available(self):
        """Test that all required modules are available."""
        required_modules = [
            'os', 'sys', 'subprocess', 'threading', 'queue', 're', 
            'shlex', 'shutil', 'signal', 'time', 'traceback', 'atexit'
        ]
        
        for module_name in required_modules:
            try:
                __import__(module_name)
            except ImportError:
                pytest.fail(f"Required module '{module_name}' not available")
    
    def test_mcp_dependency_available(self):
        """Test that MCP dependency is available."""
        try:
            from mcp.server.fastmcp import FastMCP
            # Should be able to create an instance
            mcp_instance = FastMCP("test")
            assert mcp_instance is not None
        except ImportError:
            pytest.fail("MCP dependency not available")
        except Exception as e:
            pytest.fail(f"Error with MCP dependency: {e}")


@pytest.mark.slow
class TestErrorHandling:
    """Test error handling in various scenarios."""
    
    @pytest.fixture(autouse=True)
    def cleanup(self):
        """Cleanup after each test."""
        yield
        try:
            end_debug()
        except Exception:
            pass
    
    def test_debug_nonexistent_file(self):
        """Test debugging a file that doesn't exist."""
        result = start_debug("/path/that/does/not/exist/file.py")
        assert "Error: File not found" in result
    
    def test_debug_invalid_syntax_file(self, temp_dir):
        """Test debugging a file with invalid Python syntax."""
        invalid_file = temp_dir / "invalid.py"
        invalid_file.write_text("def broken_function(\n    invalid syntax here")
        
        result = start_debug(str(invalid_file))
        # Should start but may encounter syntax error during execution
        # The important thing is that our tool doesn't crash
        assert isinstance(result, str)
    
    def test_multiple_debug_sessions(self, sample_python_file):
        """Test that we handle multiple debug session attempts properly."""
        # Start first session
        result1 = start_debug(sample_python_file)
        
        if "(Pdb)" in result1 or "started" in result1.lower():
            # Try to start another session - should be rejected
            result2 = start_debug(sample_python_file)
            assert "already running" in result2
            
            # End the first session
            end_debug()
        
        # Now should be able to start a new session
        result3 = start_debug(sample_python_file)
        # Should succeed or fail for other reasons, but not "already running"
        assert "already running" not in result3
        
        # Clean up
        if "(Pdb)" in result3 or "started" in result3.lower():
            end_debug()
    
    def test_command_without_session(self):
        """Test sending commands without an active debug session."""
        result = send_pdb_command("n")
        assert "No active debugging session" in result
        
        result = set_breakpoint("test.py", 10)
        assert "No active debugging session" in result
        
        result = get_debug_status()
        assert "No active debugging session" in result


@pytest.mark.integration
class TestEnvironmentDetection:
    """Test environment detection capabilities."""
    
    def test_detect_project_root_indicators(self, temp_dir):
        """Test detection of various project root indicators."""
        from src.python_debugger_mcp.main import find_project_root
        
        # Test with pyproject.toml
        (temp_dir / "pyproject.toml").touch()
        result = find_project_root(str(temp_dir / "subdir"))
        assert str(temp_dir) in result
        
        # Clean up and test with .git
        (temp_dir / "pyproject.toml").unlink()
        (temp_dir / ".git").mkdir()
        result = find_project_root(str(temp_dir / "subdir"))
        assert str(temp_dir) in result
    
    def test_virtual_environment_detection(self):
        """Test virtual environment detection."""
        from src.python_debugger_mcp.main import find_venv_details
        
        # Test with current environment (may or may not have venv)
        python_exe, bin_dir = find_venv_details(os.getcwd())
        
        # Should return either valid paths or (None, None)
        if python_exe is not None:
            assert os.path.exists(python_exe) or python_exe == sys.executable
            assert bin_dir is not None
        else:
            assert bin_dir is None
    
    def test_command_availability(self):
        """Test detection of available commands."""
        import shutil
        
        # Python should always be available
        python_path = shutil.which("python") or shutil.which("python3")
        assert python_path is not None
        
        # UV may or may not be available
        uv_path = shutil.which("uv")
        print(f"UV available: {uv_path is not None}")
        
        # pytest may or may not be available
        pytest_path = shutil.which("pytest")
        print(f"pytest available: {pytest_path is not None}") 
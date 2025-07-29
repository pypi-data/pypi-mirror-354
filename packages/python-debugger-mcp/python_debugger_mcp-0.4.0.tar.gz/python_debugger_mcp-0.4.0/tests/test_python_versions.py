"""Tests specifically for Python version compatibility."""

import sys
import pytest
from packaging import version
import subprocess
import importlib.util


class TestPythonVersionSupport:
    """Test support for different Python versions."""
    
    def test_minimum_python_version(self):
        """Test that we're running on a supported Python version."""
        current_version = version.Version(f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        
        # This will help us determine what minimum version we can support
        print(f"Current Python version: {current_version}")
        
        # Check if we're at least Python 3.6 (for f-strings)
        min_version = version.Version("3.6.0")
        assert current_version >= min_version, f"Python {current_version} is below minimum supported version {min_version}"
    
    def test_f_string_support(self):
        """Test f-string support (Python 3.6+)."""
        name = "test"
        value = 42
        
        # This should work on Python 3.6+
        result = f"Hello {name}, value is {value}"
        assert result == "Hello test, value is 42"
    
    def test_pathlib_support(self):
        """Test pathlib support (Python 3.4+)."""
        from pathlib import Path
        
        # Create a path
        path = Path("/tmp") / "test.txt"
        assert str(path) == "/tmp/test.txt"
    
    def test_typing_support(self):
        """Test typing module support (Python 3.5+)."""
        from typing import List, Dict, Optional, Union
        
        # These should be available
        def example_function(items: List[str]) -> Dict[str, Optional[Union[str, int]]]:
            return {item: len(item) for item in items}
        
        result = example_function(["hello", "world"])
        assert result == {"hello": 5, "world": 5}
    
    def test_asyncio_support(self):
        """Test asyncio support (Python 3.7+ features)."""
        import asyncio
        
        # Test basic asyncio functionality
        async def async_function():
            return "async_result"
        
        # Run the async function (Python 3.7+ syntax)
        try:
            result = asyncio.run(async_function())
            assert result == "async_result"
            asyncio_available = True
        except AttributeError:
            # asyncio.run() not available in Python < 3.7
            asyncio_available = False
        
        # Record the result for version compatibility analysis
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"Python {python_version}: asyncio.run() available: {asyncio_available}")
    
    def test_dataclasses_support(self):
        """Test dataclasses support (Python 3.7+)."""
        try:
            from dataclasses import dataclass, field
            
            @dataclass
            class TestClass:
                name: str
                value: int = field(default=0)
            
            obj = TestClass("test", 42)
            assert obj.name == "test"
            assert obj.value == 42
            dataclasses_available = True
        except ImportError:
            dataclasses_available = False
        
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"Python {python_version}: dataclasses available: {dataclasses_available}")
    
    def test_walrus_operator_support(self):
        """Test walrus operator support (Python 3.8+)."""
        # We don't use walrus operator in our code, but test if it's available
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        try:
            # Test walrus operator in a safe way
            code = "if (n := 42) > 40: result = n"
            compile(code, '<string>', 'exec')
            walrus_available = True
        except SyntaxError:
            walrus_available = False
        
        print(f"Python {python_version}: walrus operator available: {walrus_available}")
    
    def test_match_case_support(self):
        """Test match/case support (Python 3.10+)."""
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        try:
            # Test match/case in a safe way
            code = """
def test_match(value):
    match value:
        case 1:
            return "one"
        case _:
            return "other"
"""
            compile(code, '<string>', 'exec')
            match_case_available = True
        except SyntaxError:
            match_case_available = False
        
        print(f"Python {python_version}: match/case available: {match_case_available}")
    
    def test_required_stdlib_modules(self):
        """Test that all required standard library modules are available."""
        required_modules = [
            'os', 'sys', 'subprocess', 'threading', 'queue', 'time',
            're', 'shlex', 'shutil', 'signal', 'traceback', 'atexit'
        ]
        
        missing_modules = []
        for module_name in required_modules:
            try:
                __import__(module_name)
            except ImportError:
                missing_modules.append(module_name)
        
        assert not missing_modules, f"Missing required modules: {missing_modules}"
    
    def test_subprocess_features(self):
        """Test subprocess features used in the code."""
        import subprocess
        
        # Test subprocess.run (Python 3.5+)
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            assert result.returncode == 0
            run_available = True
        except (AttributeError, TypeError):
            run_available = False
        
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"Python {python_version}: subprocess.run available: {run_available}")
        
        # Test subprocess.Popen (should always be available)
        process = subprocess.Popen([sys.executable, '--version'], 
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        assert process.returncode == 0
    
    def test_threading_features(self):
        """Test threading features used in the code."""
        import threading
        import queue
        import time
        
        # Test threading.Thread (should always be available)
        test_queue = queue.Queue()
        
        def worker():
            test_queue.put("test_message")
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        thread.join(timeout=1.0)
        
        assert not test_queue.empty()
        assert test_queue.get() == "test_message"
    
    def test_pathlib_features(self):
        """Test pathlib features that might be version-dependent."""
        from pathlib import Path
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "test.txt"
            
            # Test write_text/read_text (Python 3.5+)
            try:
                path.write_text("test content")
                content = path.read_text()
                assert content == "test content"
                pathlib_text_methods = True
            except AttributeError:
                pathlib_text_methods = False
            
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
            print(f"Python {python_version}: pathlib text methods available: {pathlib_text_methods}")


@pytest.mark.parametrize("python_version", ["3.9", "3.10", "3.11", "3.12", "3.13"])
def test_version_compatibility_info(python_version):
    """Test to document version compatibility information."""
    current = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    if current == python_version:
        print(f"✓ Currently testing on Python {python_version}")
    else:
        print(f"- Python {python_version} not being tested (current: {current})")


class TestMCPCompatibility:
    """Test MCP library compatibility."""
    
    def test_mcp_import(self):
        """Test that MCP library can be imported."""
        try:
            from mcp.server.fastmcp import FastMCP
            mcp_available = True
            
            # Test creating an instance
            mcp_instance = FastMCP("test")
            assert mcp_instance is not None
            
        except ImportError as e:
            mcp_available = False
            print(f"MCP import failed: {e}")
        
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        print(f"Python {python_version}: MCP library available: {mcp_available}")
        
        # MCP should be available if we're running these tests
        assert mcp_available, "MCP library should be available for testing"
    
    def test_mcp_tool_decorator(self):
        """Test MCP tool decorator functionality."""
        from mcp.server.fastmcp import FastMCP
        
        mcp = FastMCP("test")
        
        @mcp.tool()
        def test_tool(message: str) -> str:
            """A test tool."""
            return f"Hello {message}"
        
        # Should be able to create the tool without errors
        assert callable(test_tool)
        result = test_tool("world")
        assert result == "Hello world"


if __name__ == "__main__":
    # Run version compatibility tests
    pytest.main([__file__, "-v"]) 
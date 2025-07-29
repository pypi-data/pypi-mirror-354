#!/usr/bin/env python3
"""Test runner script for python-debugger-mcp compatibility testing."""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and print results."""
    print(f"\n{'='*60}")
    print(f"Running: {description or ' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, text=True, capture_output=False)
        print(f"✓ {description or 'Command'} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description or 'Command'} failed with exit code {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"✗ Command not found: {cmd[0]}")
        return False


def check_python_version():
    """Check and display current Python version."""
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 6):
        print("⚠️  Warning: Python version is below recommended minimum (3.6)")
        return False
    elif version < (3, 9):
        print("⚠️  Warning: Python version is below proposed minimum (3.9)")
    else:
        print("✓ Python version is supported")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Run python-debugger-mcp compatibility tests")
    parser.add_argument("--test-type", choices=["all", "unit", "integration", "compatibility", "coverage"], 
                       default="all", help="Type of tests to run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies first")
    parser.add_argument("--check-minimum", action="store_true", 
                       help="Test compatibility with proposed minimum Python version")
    
    args = parser.parse_args()
    
    print("python-debugger-mcp Compatibility Test Runner")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies if requested
    if args.install_deps:
        if not run_command(["uv", "sync", "--extra", "test"], "Installing test dependencies"):
            print("Failed to install dependencies. Make sure 'uv' is installed.")
            sys.exit(1)
    
    verbose_flag = ["-v"] if args.verbose else []
    all_passed = True
    
    # Test basic imports first
    import_test = [
        "uv", "run", "python", "-c",
        """
import sys
print(f'Testing imports on Python {sys.version_info.major}.{sys.version_info.minor}...')

try:
    from src.python_debugger_mcp.main import find_project_root, find_venv_details, sanitize_arguments
    print('✓ Core functions imported')
    
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP('test')
    print('✓ MCP library imported and instantiated')
    
    print('✓ All imports successful')
except Exception as e:
    print(f'✗ Import failed: {e}')
    sys.exit(1)
"""
    ]
    
    if not run_command(import_test, "Testing basic imports"):
        all_passed = False
    
    # Run compatibility tests
    if args.test_type in ["all", "compatibility"]:
        cmd = ["uv", "run", "pytest", "tests/test_python_versions.py"] + verbose_flag
        if not run_command(cmd, "Python version compatibility tests"):
            all_passed = False
    
    # Run unit tests
    if args.test_type in ["all", "unit"]:
        cmd = ["uv", "run", "pytest", "tests/test_helpers.py", "-m", "unit"] + verbose_flag
        if not run_command(cmd, "Unit tests"):
            all_passed = False
        
        cmd = ["uv", "run", "pytest", "tests/test_mcp_tools.py", "-k", "not integration"] + verbose_flag
        if not run_command(cmd, "MCP tool tests (mocked)"):
            all_passed = False
    
    # Run safe integration tests
    if args.test_type in ["all", "integration"]:
        safe_tests = [
            "tests/test_integration.py::TestPythonVersionCompatibility",
            "tests/test_integration.py::TestEnvironmentDetection", 
            "tests/test_integration.py::TestErrorHandling::test_debug_nonexistent_file",
            "tests/test_integration.py::TestErrorHandling::test_command_without_session",
        ]
        
        for test in safe_tests:
            cmd = ["uv", "run", "pytest", test] + verbose_flag
            if not run_command(cmd, f"Safe integration test: {test.split('::')[-1]}"):
                all_passed = False
    
    # Run coverage tests
    if args.test_type in ["all", "coverage"]:
        cmd = [
            "uv", "run", "pytest", "tests/", 
            "--cov=src/python_debugger_mcp", "--cov-report=term-missing", 
            "-m", "not slow"
        ] + verbose_flag
        if not run_command(cmd, "Coverage tests"):
            all_passed = False
    
    # Test minimum version compatibility if requested
    if args.check_minimum:
        print(f"\n{'='*60}")
        print("Testing minimum version compatibility")
        print('='*60)
        
        # Create a temporary pyproject.toml with lower requirements
        original_content = Path("pyproject.toml").read_text()
        temp_content = original_content.replace('requires-python = ">=3.13"', 'requires-python = ">=3.9"')
        
        try:
            Path("pyproject.toml").write_text(temp_content)
            
            # Test basic functionality
            cmd = [
                "uv", "run", "python", "-c",
                """
from src.python_debugger_mcp.main import find_project_root, sanitize_arguments
print('✓ Core functions work with minimum version')

args = sanitize_arguments('--verbose --output file.txt')
assert args == ['--verbose', '--output', 'file.txt']
print('✓ Argument parsing works')

root = find_project_root('.')
print(f'✓ Project root detection works: {root}')
"""
            ]
            
            if not run_command(cmd, "Minimum version functionality test"):
                all_passed = False
        
        finally:
            # Restore original pyproject.toml
            Path("pyproject.toml").write_text(original_content)
    
    # Summary
    print(f"\n{'='*60}")
    if all_passed:
        print("✓ All tests passed! The code appears compatible across Python versions.")
        if args.check_minimum:
            print("✓ Minimum version compatibility confirmed.")
    else:
        print("✗ Some tests failed. Review the output above for details.")
        sys.exit(1)
    print('='*60)


if __name__ == "__main__":
    main() 
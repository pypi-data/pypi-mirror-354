# python-debugger-mcp Test Suite

This directory contains comprehensive tests for the python-debugger-mcp project, specifically designed to verify compatibility when lowering Python version requirements from 3.13 to earlier versions.

## Test Structure

### Core Test Files

- **`test_helpers.py`** - Unit tests for helper functions

  - `find_project_root()` - Project root detection
  - `find_venv_details()` - Virtual environment detection
  - `sanitize_arguments()` - Argument parsing
  - `get_pdb_output()` - PDB output handling
  - Python compatibility features testing

- **`test_mcp_tools.py`** - Unit tests for MCP tools

  - `start_debug()` - Debug session initialization
  - `send_pdb_command()` - Command sending
  - Breakpoint management (`set_breakpoint`, `clear_breakpoint`, `list_breakpoints`)
  - Variable examination (`examine_variable`)
  - Session management (`restart_debug`, `end_debug`, `get_debug_status`)

- **`test_integration.py`** - Integration tests with real processes

  - Real Python script debugging
  - Environment detection
  - Error handling scenarios
  - Cross-version compatibility verification

- **`test_python_versions.py`** - Python version compatibility tests
  - Feature availability testing (f-strings, pathlib, typing, etc.)
  - Standard library module verification
  - MCP dependency compatibility
  - Version-specific feature detection

### Supporting Files

- **`conftest.py`** - Pytest configuration and shared fixtures

  - Temporary directories and test files
  - Mock subprocess operations
  - Global state reset utilities
  - Environment detection mocks

- **`README.md`** - This documentation file

## Running Tests

### Quick Start

1. **Install test dependencies:**

   ```bash
   uv sync --extra test
   ```

2. **Run all tests:**

   ```bash
   python run_tests.py --install-deps
   ```

3. **Test minimum version compatibility:**
   ```bash
   python run_tests.py --check-minimum
   ```

### Detailed Testing Options

#### Using the Test Runner Script

```bash
# Run all tests with verbose output
python run_tests.py --verbose

# Run only unit tests
python run_tests.py --test-type unit

# Run only compatibility tests
python run_tests.py --test-type compatibility

# Run integration tests (safe subset)
python run_tests.py --test-type integration

# Run with coverage reporting
python run_tests.py --test-type coverage

# Test minimum Python version compatibility
python run_tests.py --check-minimum --verbose
```

#### Using pytest Directly

```bash
# Run specific test categories
uv run pytest tests/test_python_versions.py -v
uv run pytest tests/test_helpers.py -m unit -v
uv run pytest tests/test_mcp_tools.py -k "not integration" -v

# Run with coverage
uv run pytest tests/ --cov=src/python_debugger_mcp --cov-report=term-missing

# Run only fast tests (exclude slow integration tests)
uv run pytest tests/ -m "not slow" -v
```

## Test Categories

Tests are organized with pytest markers:

- **`@pytest.mark.unit`** - Fast unit tests
- **`@pytest.mark.integration`** - Integration tests requiring real processes
- **`@pytest.mark.slow`** - Slower tests that may timeout or require special setup

## Python Version Compatibility Testing

### Current Status

The codebase currently requires Python 3.13, but analysis shows it can work with earlier versions:

- **Python 3.6+**: Core functionality (f-strings, basic features)
- **Python 3.9+**: Recommended minimum (better subprocess support, pathlib features)
- **Python 3.11+**: Full feature compatibility

### Compatibility Test Results

Run `python run_tests.py --test-type compatibility` to see detailed compatibility information:

```
Python X.Y: feature_name available: True/False
```

### Lowering Version Requirements

To test lowering the Python requirement:

1. **Test current compatibility:**

   ```bash
   python run_tests.py --check-minimum
   ```

2. **Update `pyproject.toml`:**

   ```toml
   requires-python = ">=3.9"  # or desired minimum version
   ```

3. **Test with target Python version:**

   ```bash
   # Using pyenv or conda
   pyenv local 3.9.18
   python run_tests.py --install-deps

   # Or using specific Python
   python3.9 run_tests.py --install-deps
   ```

4. **Run full test suite:**
   ```bash
   python run_tests.py --verbose
   ```

## Continuous Integration

The `.github/workflows/test.yml` workflow automatically tests:

- **Compatibility**: Python 3.9, 3.10, 3.11, 3.12, 3.13
- **Integration**: Safe subset on Python 3.9, 3.11, 3.13
- **Minimum Version**: Validates Python 3.9 compatibility
- **Coverage**: Code coverage reporting

## Key Compatibility Considerations

### Dependencies

1. **MCP Library**: Verify `mcp[cli]>=1.6.0` supports target Python version
2. **Standard Library**: All required modules available in target version
3. **Third-party**: Test dependencies support target version

### Language Features

- **F-strings** (3.6+): Used throughout codebase
- **Type hints** (3.5+): Basic type hints used
- **Pathlib** (3.4+): Used for file operations
- **subprocess.run()** (3.5+): Used for process management

### Potential Issues

1. **AsyncIO**: Some features require Python 3.7+
2. **Dataclasses**: Available in 3.7+ (not currently used)
3. **Match/Case**: Available in 3.10+ (not currently used)
4. **Walrus Operator**: Available in 3.8+ (not currently used)

## Adding New Tests

### For New Features

1. Add unit tests in appropriate test file
2. Add integration tests if feature interacts with external processes
3. Add compatibility tests if feature uses version-specific Python features
4. Update markers (`@pytest.mark.unit`, etc.)

### For Version Compatibility

1. Add feature detection test in `test_python_versions.py`
2. Test both availability and functionality
3. Document minimum required version
4. Add to CI workflow if needed

## Troubleshooting

### Common Issues

1. **Import Errors**: Check dependencies are installed with `uv sync --extra test`
2. **Path Issues**: Ensure tests run from project root
3. **Permission Errors**: Check file permissions on test scripts
4. **Subprocess Timeouts**: Some integration tests may timeout on slow systems

### Debug Test Failures

```bash
# Run with maximum verbosity
python run_tests.py --verbose --test-type unit

# Run specific failing test
uv run pytest tests/test_helpers.py::TestFindProjectRoot::test_find_project_root_with_pyproject_toml -v -s

# Check Python environment
uv run python -c "import sys; print(sys.version); print(sys.path)"
```

## Contributing

When adding new functionality:

1. Write unit tests first
2. Add integration tests for external interactions
3. Test compatibility across Python versions
4. Update documentation and CI workflows
5. Verify tests pass locally before submitting PR

For more information about the python-debugger-mcp project, see the main README.md file.

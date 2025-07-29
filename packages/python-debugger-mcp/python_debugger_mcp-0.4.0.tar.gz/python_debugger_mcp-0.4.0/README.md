# Python Debugger MCP

A Model Context Protocol (MCP) server that provides Python debugging capabilities for AI assistants like Claude. This tool allows AI assistants to debug Python code by providing interactive debugging session management, breakpoint control, variable inspection, and step-by-step execution.

## Features

- **Debug Session Management**: Start, restart, and end debugging sessions
- **Breakpoint Control**: Set, clear, and list breakpoints
- **Variable Inspection**: Examine variable values during debugging
- **Step Execution**: Step through code line by line
- **Environment Detection**: Automatically detect Python environments and project structure
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

```bash
pip install python-debugger-mcp
```

## Usage

### As an MCP Server

Run the server directly:

```bash
python-debugger-mcp
```

### In Claude Desktop

Add this to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "python-debugger": {
      "command": "python-debugger-mcp"
    }
  }
}
```

### Available Tools

The MCP server provides these debugging tools:

- `start_debug(script_path)` - Start debugging a Python script
- `send_pdb_command(command)` - Send commands to the debugger
- `set_breakpoint(file_path, line_number)` - Set a breakpoint
- `clear_breakpoint(file_path, line_number)` - Clear a breakpoint
- `list_breakpoints()` - List all breakpoints
- `examine_variable(variable_name)` - Examine a variable's value
- `restart_debug()` - Restart the current debugging session
- `end_debug()` - End the debugging session
- `get_debug_status()` - Get current debugging status

## Requirements

- Python 3.10 or higher
- MCP library support

## Development

### Installing for Development

```bash
git clone <repository-url>
cd python-debugger-mcp
uv sync
```

### Running Tests

```bash
python run_tests.py --test-type all
```

## License

MIT License - see LICENSE file for details.

## Inspiration

This project was inspired by [debug-gym](https://microsoft.github.io/debug-gym/), which provides debugging environments for AI agents.

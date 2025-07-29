"""Unit tests for MCP tools in python-debugger-mcp."""

import pytest
from unittest.mock import patch, Mock, MagicMock
import os
import subprocess

# Import the MCP tool functions
from src.python_debugger_mcp.main import (
    start_debug,
    send_pdb_command,
    set_breakpoint,
    clear_breakpoint,
    list_breakpoints,
    restart_debug,
    examine_variable,
    get_debug_status,
    end_debug,
)


class TestStartDebug:
    """Tests for start_debug MCP tool."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    @patch('src.python_debugger_mcp.main.subprocess.Popen')
    @patch('src.python_debugger_mcp.main.threading.Thread')
    @patch('src.python_debugger_mcp.main.get_pdb_output')
    @patch('src.python_debugger_mcp.main.find_project_root')
    @patch('os.path.exists')
    @patch('shutil.which')
    def test_start_debug_success(self, mock_which, mock_exists, mock_find_root, 
                                mock_get_output, mock_thread, mock_popen, sample_python_file):
        """Test successful debug session start."""
        # Setup mocks
        mock_which.return_value = "/usr/bin/python"
        mock_exists.return_value = True
        mock_find_root.return_value = "/project/root"
        mock_get_output.return_value = "-> 1 def add_numbers(a, b):\n(Pdb)"
        
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.stdout = Mock() 
        mock_popen.return_value = mock_process
        
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        # Call the function
        result = start_debug(sample_python_file)
        
        # Verify results
        assert "Debugging session started" in result or "(Pdb)" in result
        mock_popen.assert_called_once()
        mock_thread_instance.start.assert_called_once()
    
    def test_start_debug_file_not_found(self, reset_global_state):
        """Test start_debug with non-existent file."""
        result = start_debug("/non/existent/file.py")
        assert "Error: File not found" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.pdb_process')
    def test_start_debug_already_running(self, mock_process, reset_global_state):
        """Test start_debug when session already running."""
        mock_process.poll.return_value = None  # Process is running
        
        result = start_debug("/some/file.py")
        assert "already running" in result
    
    @patch('src.python_debugger_mcp.main.subprocess.Popen')
    @patch('os.path.exists')
    @patch('shutil.which')
    def test_start_debug_with_pytest(self, mock_which, mock_exists, mock_popen, 
                                   sample_python_file, reset_global_state):
        """Test start_debug with pytest option."""
        mock_which.side_effect = lambda x: "/usr/bin/pytest" if x == "pytest" else "/usr/bin/python"
        mock_exists.return_value = True
        
        mock_process = Mock()
        mock_process.poll.return_value = 1  # Process exits immediately (for this test)
        mock_process.communicate.return_value = (b"test output", b"")
        mock_popen.return_value = mock_process
        
        result = start_debug(sample_python_file, use_pytest=True)
        
        # Verify pytest was used in the command
        call_args = mock_popen.call_args[0][0]  # Get the command arguments
        assert "pytest" in call_args
        assert "--pdb" in call_args


class TestSendPdbCommand:
    """Tests for send_pdb_command MCP tool."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    def test_send_pdb_command_no_session(self, reset_global_state):
        """Test sending command when no debug session is active."""
        result = send_pdb_command("n")
        assert "No active debugging session" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    def test_send_pdb_command_success(self, mock_send_to_pdb, reset_global_state):
        """Test successful command sending."""
        mock_send_to_pdb.return_value = "-> 2 result = a + b\n(Pdb)"
        
        result = send_pdb_command("n")
        
        assert "Command output:" in result
        mock_send_to_pdb.assert_called_once_with("n", 1.0)
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.pdb_process')
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    def test_send_navigation_command(self, mock_send_to_pdb, mock_process, reset_global_state):
        """Test sending navigation command with context."""
        mock_process.poll.return_value = None  # Process is running
        mock_send_to_pdb.side_effect = [
            "-> 2 result = a + b\n(Pdb)",  # First call for 'n'
            "1 def add_numbers(a, b):\n-> 2 result = a + b\n3 return result"  # Second call for 'l .'
        ]
        
        result = send_pdb_command("n")
        
        assert "Command output:" in result
        assert "Current location" in result
        assert mock_send_to_pdb.call_count == 2


class TestBreakpointManagement:
    """Tests for breakpoint-related MCP tools."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    def test_set_breakpoint_no_session(self, reset_global_state):
        """Test setting breakpoint when no debug session is active."""
        result = set_breakpoint("/some/file.py", 10)
        assert "No active debugging session" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.current_project_root', '/project/root')
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    @patch('os.path.exists')
    def test_set_breakpoint_success(self, mock_exists, mock_send_to_pdb, reset_global_state):
        """Test successful breakpoint setting."""
        mock_exists.return_value = True
        mock_send_to_pdb.return_value = "Breakpoint 1 at /project/root/file.py:10"
        
        result = set_breakpoint("file.py", 10)
        
        assert "Breakpoint #1 set and tracked" in result
        mock_send_to_pdb.assert_called_once()
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.current_project_root', '/project/root')
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    @patch('os.path.exists')
    def test_clear_breakpoint_success(self, mock_exists, mock_send_to_pdb, reset_global_state):
        """Test successful breakpoint clearing."""
        # Set up existing breakpoint
        import src.python_debugger_mcp.main as main_module
        abs_path = "/project/root/file.py"
        main_module.breakpoints[abs_path] = {10: {"command": "b file.py:10", "bp_number": "1"}}
        
        mock_exists.return_value = True
        mock_send_to_pdb.return_value = "Deleted breakpoint 1 at /project/root/file.py:10"
        
        result = clear_breakpoint("file.py", 10)
        
        assert "Clear breakpoint result:" in result
        assert "untracked" in result
        mock_send_to_pdb.assert_called_once()
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.current_project_root', '/project/root')
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    def test_list_breakpoints(self, mock_send_to_pdb, reset_global_state):
        """Test listing breakpoints."""
        # Set up existing breakpoints
        import src.python_debugger_mcp.main as main_module
        abs_path = "/project/root/file.py"
        main_module.breakpoints[abs_path] = {
            10: {"command": "b file.py:10", "bp_number": "1"},
            20: {"command": "b file.py:20", "bp_number": "2"}
        }
        
        mock_send_to_pdb.return_value = "Num Type         Disp Enb   Where\n1   breakpoint   keep yes   at /project/root/file.py:10"
        
        result = list_breakpoints()
        
        assert "PDB Breakpoints" in result
        assert "Tracked Breakpoints" in result
        assert "file.py:10 (BP #1)" in result
        assert "file.py:20 (BP #2)" in result


class TestVariableExamination:
    """Tests for examine_variable MCP tool."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    def test_examine_variable_no_session(self, reset_global_state):
        """Test examining variable when no debug session is active."""
        result = examine_variable("my_var")
        assert "No active debugging session" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    def test_examine_variable_success(self, mock_send_to_pdb, reset_global_state):
        """Test successful variable examination."""
        mock_send_to_pdb.side_effect = [
            "42",  # p my_var
            "42",  # pp my_var  
            "<class 'int'>",  # p type(my_var)
            "['__abs__', '__add__', ...]"  # p dir(my_var)
        ]
        
        result = examine_variable("my_var")
        
        assert "Variable Examination: my_var" in result
        assert "Value (p):" in result
        assert "Pretty Value (pp):" in result
        assert "Type" in result
        assert "Attributes/Methods" in result
        assert mock_send_to_pdb.call_count == 4


class TestDebugStatus:
    """Tests for get_debug_status MCP tool."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    def test_debug_status_no_session(self, reset_global_state):
        """Test debug status when no session is active."""
        result = get_debug_status()
        assert "No active debugging session" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.current_file', '/project/test.py')
    @patch('src.python_debugger_mcp.main.current_project_root', '/project')
    @patch('src.python_debugger_mcp.main.current_args', '--verbose')
    @patch('src.python_debugger_mcp.main.current_use_pytest', False)
    @patch('src.python_debugger_mcp.main.send_to_pdb')
    def test_debug_status_with_session(self, mock_send_to_pdb, reset_global_state):
        """Test debug status with active session."""
        mock_send_to_pdb.side_effect = [
            "-> 5 result = a + b\n(Pdb)",  # where command
            "a = 5\nb = 10"  # args command
        ]
        
        result = get_debug_status()
        
        assert "Debug Session Status" in result
        assert "File: /project/test.py" in result
        assert "Project: /project" in result
        assert "Arguments: --verbose" in result
        assert "Using pytest: No" in result


class TestRestartDebug:
    """Tests for restart_debug MCP tool."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    def test_restart_debug_no_session(self, reset_global_state):
        """Test restart when no session is active."""
        result = restart_debug()
        assert "No active debugging session" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.current_file', '/project/test.py')
    @patch('src.python_debugger_mcp.main.end_debug')
    @patch('src.python_debugger_mcp.main.start_debug')
    def test_restart_debug_success(self, mock_start, mock_end, reset_global_state):
        """Test successful debug restart."""
        mock_end.return_value = "Debug session ended"
        mock_start.return_value = "Debug session started"
        
        result = restart_debug()
        
        assert "Restarting debugging session" in result
        mock_end.assert_called_once()
        mock_start.assert_called_once()


class TestEndDebug:
    """Tests for end_debug MCP tool."""
    
    @pytest.fixture(autouse=True)
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    def test_end_debug_no_session(self, reset_global_state):
        """Test ending debug when no session is active."""
        result = end_debug()
        assert "No active debugging session" in result
    
    @patch('src.python_debugger_mcp.main.pdb_running', True)
    @patch('src.python_debugger_mcp.main.pdb_process')
    @patch('src.python_debugger_mcp.main.output_thread')
    @patch('src.python_debugger_mcp.main.get_pdb_output')
    def test_end_debug_success(self, mock_get_output, mock_thread, mock_process, reset_global_state):
        """Test successful debug session end."""
        mock_process.poll.return_value = None
        mock_process.terminate.return_value = None
        mock_process.wait.return_value = 0
        mock_thread.is_alive.return_value = False
        mock_get_output.return_value = "Final output"
        
        result = end_debug()
        
        assert "Debugging session ended" in result
        mock_process.terminate.assert_called_once()


@pytest.mark.integration
class TestMCPToolsIntegration:
    """Integration tests for MCP tools working together."""
    
    @pytest.fixture(autouse=True)  
    def setup(self, reset_global_state):
        """Setup for each test."""
        pass
    
    @patch('src.python_debugger_mcp.main.subprocess.Popen')
    @patch('src.python_debugger_mcp.main.threading.Thread')
    @patch('src.python_debugger_mcp.main.get_pdb_output')
    @patch('os.path.exists')
    @patch('shutil.which')
    def test_full_debug_workflow(self, mock_which, mock_exists, mock_get_output, 
                                 mock_thread, mock_popen, sample_python_file, reset_global_state):
        """Test a complete debugging workflow."""
        # Setup mocks
        mock_which.return_value = "/usr/bin/python"
        mock_exists.return_value = True
        mock_get_output.return_value = "-> 1 def add_numbers(a, b):\n(Pdb)"
        
        mock_process = Mock()
        mock_process.poll.return_value = None
        mock_process.stdin = Mock()
        mock_process.stdout = Mock()
        mock_popen.return_value = mock_process
        
        mock_thread_instance = Mock()
        mock_thread.return_value = mock_thread_instance
        
        # 1. Start debug session
        with patch('src.python_debugger_mcp.main.find_project_root', return_value="/project"):
            start_result = start_debug(sample_python_file)
            assert "(Pdb)" in start_result
        
        # 2. Check status
        with patch('src.python_debugger_mcp.main.send_to_pdb', return_value="-> 1 def add_numbers(a, b):"):
            status_result = get_debug_status()
            assert "Debug Session Status" in status_result
        
        # 3. Set breakpoint
        with patch('src.python_debugger_mcp.main.send_to_pdb', return_value="Breakpoint 1 at"):
            bp_result = set_breakpoint("test_script.py", 5)
            assert "set and tracked" in bp_result
        
        # 4. End session
        end_result = end_debug()
        assert "ended" in end_result 
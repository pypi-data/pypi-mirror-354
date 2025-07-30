"""
Unit tests for VibeBash class
"""
import json
import subprocess
from unittest.mock import Mock, patch, mock_open
import pytest

from vibebash.main import VibeBash, Command


class TestVibeBashInit:
    """Test VibeBash initialization"""
    
    def test_init_with_defaults(self, temp_config_dir):
        """Test initialization with default values"""
        with patch('vibebash.main.VibeBash.setup_llm'), \
             patch('vibebash.main.VibeBash.load_config'):
            vb = VibeBash()
            assert vb.history_file.name == ".vibebash_history.json"
            assert vb.config_file.name == ".vibebash_config.json"
    
    def test_init_with_custom_model(self, temp_config_dir):
        """Test initialization with custom model"""
        with patch('vibebash.main.VibeBash.setup_llm') as mock_setup, \
             patch('vibebash.main.VibeBash.load_config'):
            VibeBash(model_name="deepcoder")
            mock_setup.assert_called_with("deepcoder")


class TestConfigManagement:
    """Test configuration management"""
    
    def test_load_existing_config(self, temp_config_dir, mock_config):
        """Test loading existing configuration"""
        config_file = temp_config_dir / ".vibebash_config.json"
        config_file.write_text(json.dumps(mock_config))
        
        with patch('vibebash.main.VibeBash.setup_llm'):
            vb = VibeBash()
            assert vb.config == mock_config
    
    def test_create_new_config(self, temp_config_dir):
        """Test creating new configuration"""
        with patch('vibebash.main.VibeBash.setup_llm'), \
             patch('vibebash.main.Prompt.ask') as mock_prompt:
            
            mock_prompt.side_effect = [
                "http://localhost:11434",
                "llama3.2"
            ]
            
            vb = VibeBash()
            
            assert vb.config["ollama_base_url"] == "http://localhost:11434"
            assert vb.config["default_model_name"] == "llama3.2"


class TestSystemInfo:
    """Test system information gathering"""
    
    def test_get_system_info(self, vibebash_instance):
        """Test system info gathering"""
        with patch('platform.system', return_value='Linux'), \
             patch('platform.release', return_value='5.4.0'), \
             patch('os.getcwd', return_value='/home/user'), \
             patch('os.getenv') as mock_getenv:
            
            mock_getenv.side_effect = lambda key, default=None: {
                'SHELL': '/bin/bash',
                'USER': 'testuser'
            }.get(key, default)
            
            info = vibebash_instance.get_system_info()
            
            assert 'Linux 5.4.0' in info
            assert '/home/user' in info
            assert '/bin/bash' in info
            assert 'testuser' in info
    
    def test_get_system_info_exception(self, vibebash_instance):
        """Test system info when exception occurs"""
        with patch('platform.system', side_effect=Exception("Test error")):
            info = vibebash_instance.get_system_info()
            assert info == "System info unavailable"


class TestCommandExecution:
    """Test command execution"""
    
    def test_execute_successful_command(self, vibebash_instance, mock_subprocess_success):
        """Test successful command execution"""
        with patch('subprocess.run', return_value=mock_subprocess_success):
            success, output = vibebash_instance.execute_command("ls -la")
            
            assert success is True
            assert output == "Command executed successfully"
    
    def test_execute_failed_command(self, vibebash_instance, mock_subprocess_failure):
        """Test failed command execution"""
        with patch('subprocess.run', return_value=mock_subprocess_failure):
            success, output = vibebash_instance.execute_command("invalid-command")
            
            assert success is False
            assert "invalid-command" in output  # Check that command name is in error message
    
    def test_execute_command_timeout(self, vibebash_instance):
        """Test command execution timeout"""
        with patch('subprocess.run', side_effect=subprocess.TimeoutExpired("ls", 30)):
            success, output = vibebash_instance.execute_command("sleep 60")
            
            assert success is False
            assert "timed out" in output
    
    def test_execute_command_exception(self, vibebash_instance):
        """Test command execution with exception"""
        with patch('subprocess.run', side_effect=Exception("Test error")):
            success, output = vibebash_instance.execute_command("ls")
            
            assert success is False
            assert "Error executing command" in output


class TestHistoryManagement:
    """Test command history management"""
    
    def test_load_existing_history(self, temp_config_dir, mock_config):
        """Test loading existing history"""
        history_data = [
            {
                "command": "ls -la",
                "explanation": "List files",
                "timestamp": "2024-01-01T12:00:00",
                "success": True,
                "output": "file1.txt file2.txt"
            }
        ]
        
        history_file = temp_config_dir / ".vibebash_history.json"
        history_file.write_text(json.dumps(history_data))
        
        config_file = temp_config_dir / ".vibebash_config.json"
        config_file.write_text(json.dumps(mock_config))
        
        with patch('vibebash.main.VibeBash.setup_llm'):
            vb = VibeBash()
            assert len(vb.history) == 1
            assert vb.history[0]["command"] == "ls -la"
    
    def test_load_empty_history(self, vibebash_instance):
        """Test loading when no history exists"""
        assert isinstance(vibebash_instance.history, list)
        assert len(vibebash_instance.history) == 0
    
    def test_save_to_history(self, vibebash_instance, temp_config_dir):
        """Test saving command to history"""
        from vibebash.main import ExecutedCommand
        
        exec_cmd = ExecutedCommand(
            command="pwd",
            explanation="Print working directory",
            timestamp="2024-01-01T12:00:00",
            success=True,
            output="/home/user"
        )
        
        with patch('builtins.open', mock_open()) as mock_file:
            vibebash_instance.save_to_history(exec_cmd)
            
            assert len(vibebash_instance.history) == 1
            assert vibebash_instance.history[0]["command"] == "pwd"
    
    def test_history_limit(self, vibebash_instance):
        """Test history size limit"""
        from vibebash.main import ExecutedCommand
        
        # Add more than 100 commands
        for i in range(105):
            exec_cmd = ExecutedCommand(
                command=f"echo {i}",
                explanation=f"Echo number {i}",
                timestamp="2024-01-01T12:00:00",
                success=True,
                output=str(i)
            )
            vibebash_instance.save_to_history(exec_cmd)
        
        # Should only keep last 100
        assert len(vibebash_instance.history) == 100
        assert vibebash_instance.history[0]["command"] == "echo 5"  # First 5 should be removed


class TestPromptCreation:
    """Test prompt creation for LLM"""
    
    def test_create_basic_prompt(self, vibebash_instance):
        """Test creating basic prompt"""
        with patch.object(vibebash_instance, 'get_system_info', return_value="Test system info"):
            prompt = vibebash_instance.create_prompt("list files")
            
            assert "list files" in prompt
            assert "Test system info" in prompt
            assert "IMPORTANT GUIDELINES" in prompt
    
    def test_create_prompt_with_previous_commands(self, vibebash_instance):
        """Test creating prompt with previous commands"""
        previous_cmds = ["ls -la", "pwd", "df -h"]
        
        with patch.object(vibebash_instance, 'get_system_info', return_value="Test system info"):
            prompt = vibebash_instance.create_prompt("show disk usage", previous_cmds)
            
            assert "ls -la" in prompt
            assert "pwd" in prompt
            assert "df -h" in prompt
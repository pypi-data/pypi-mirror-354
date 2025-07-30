"""
Integration tests for CLI commands
"""
import json
from unittest.mock import patch, Mock
import pytest
from click.testing import CliRunner

from vibebash.main import main, Command, CommandList


class TestCLIBasicCommands:
    """Test basic CLI command functionality"""
    
    def test_help_command(self, cli_runner):
        """Test help command"""
        result = cli_runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "VibeBash - Offline natural language to shell commands with ChatOllama" in result.output
        assert "--model-name" in result.output
        assert "--history" in result.output
    
    def test_config_flag(self, cli_runner, temp_config_dir):
        """Test config flag creates new configuration"""
        with patch('vibebash.main.VibeBash') as mock_vb_class, \
             patch('vibebash.main.Prompt.ask') as mock_prompt:
            
            mock_prompt.side_effect = [
                "http://localhost:11434",
                "llama3.2"
            ]
            
            mock_vb = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, ['--config'])
            
            assert result.exit_code == 0
            mock_vb_class.assert_called_once()
    
    def test_history_flag_empty(self, cli_runner, temp_config_dir):
        """Test history flag with empty history"""
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb = Mock()
            mock_vb.history = []
            mock_vb.console = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, ['--history'])
            
            assert result.exit_code == 0
            mock_vb.console.print.assert_called()
    
    def test_history_flag_with_data(self, cli_runner, temp_config_dir):
        """Test history flag with existing history"""
        history_data = [
            {
                "command": "ls -la",
                "timestamp": "2024-01-01T12:00:00",
                "success": True
            },
            {
                "command": "pwd",
                "timestamp": "2024-01-01T12:01:00", 
                "success": False
            }
        ]
        
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb = Mock()
            mock_vb.history = history_data
            mock_vb.console = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, ['--history'])
            
            assert result.exit_code == 0
            assert mock_vb.console.print.call_count >= 3  # Header + 2 history items


class TestCLIRequestProcessing:
    """Test CLI request processing"""
    
    @patch('asyncio.run')
    def test_process_request_with_argument(self, mock_asyncio_run, cli_runner, temp_config_dir):
        """Test processing request passed as argument"""
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, ['list files'])
            
            assert result.exit_code == 0
            mock_asyncio_run.assert_called_once()
            # Verify the async function was called with the request
            args, kwargs = mock_asyncio_run.call_args
            assert len(args) == 1  # The coroutine
    
    @patch('asyncio.run')
    @patch('vibebash.main.Prompt.ask')
    def test_process_request_interactive(self, mock_prompt, mock_asyncio_run, cli_runner, temp_config_dir):
        """Test interactive request input"""
        mock_prompt.return_value = "show disk usage"
        
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, [])
            
            assert result.exit_code == 0
            mock_prompt.assert_called_once()
            mock_asyncio_run.assert_called_once()
    
    def test_keyboard_interrupt(self, cli_runner, temp_config_dir):
        """Test handling keyboard interrupt"""
        with patch('vibebash.main.VibeBash', side_effect=KeyboardInterrupt):
            result = cli_runner.invoke(main, ['test'])
            
            # CLI should handle the interrupt gracefully
            assert "Goodbye!" in result.output or result.exit_code == 0


class TestCLIModelSelection:
    """Test CLI model selection options"""
    
    @patch('asyncio.run')
    def test_custom_model_name(self, mock_asyncio_run, cli_runner, temp_config_dir):
        """Test custom model name selection"""
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, [
                '--model-name', 'deepcoder',
                'test request'
            ])
            
            assert result.exit_code == 0
            mock_vb_class.assert_called_once_with(model_name='deepcoder')
    
    @patch('asyncio.run')
    def test_default_model_name(self, mock_asyncio_run, cli_runner, temp_config_dir):
        """Test default model name when not specified"""
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb = Mock()
            mock_vb_class.return_value = mock_vb
            
            result = cli_runner.invoke(main, [
                'test request'
            ])
            
            assert result.exit_code == 0
            mock_vb_class.assert_called_once_with()  # Should use default model


class TestCLIErrorHandling:
    """Test CLI error handling"""
    
    def test_general_exception(self, cli_runner, temp_config_dir):
        """Test handling of general exceptions"""
        with patch('vibebash.main.VibeBash', side_effect=Exception("Test error")):
            result = cli_runner.invoke(main, ['test'])
            
            assert "Error: Test error" in result.output
    
    @patch('asyncio.run')
    def test_llm_setup_failure(self, mock_asyncio_run, cli_runner, temp_config_dir):
        """Test handling LLM setup failure"""
        with patch('vibebash.main.VibeBash') as mock_vb_class:
            mock_vb_class.side_effect = Exception("Ollama connection failed")
            
            result = cli_runner.invoke(main, [
                '--model-name', 'llama3.2',
                'test request'
            ])
            
            # Should handle the exception gracefully
            assert result.exit_code == 1
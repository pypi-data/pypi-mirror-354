"""
Integration tests for full VibeBash workflows
"""
import json
from unittest.mock import Mock, patch, AsyncMock
import pytest

from vibebash.main import VibeBash, Command, CommandList
from tests.conftest import setup_mock_llm_for_workflow


class TestFullWorkflow:
    """Test complete VibeBash workflows"""
    
    @pytest.mark.asyncio
    async def test_successful_command_workflow(self, vibebash_instance, sample_commands):
        """Test complete workflow with successful command execution"""
        # Mock LLM response
        mock_response = Mock()
        mock_response.content = json.dumps({
            "commands": [
                {
                    "command": "ls -la",
                    "explanation": "List all files with details",
                    "risk_level": "low"
                }
            ]
        })
        
        # Set up mock LLM
        setup_mock_llm_for_workflow(vibebash_instance, mock_response)
        
        # Mock user input for "run" action
        with patch('vibebash.main.Prompt.ask', return_value='run'), \
             patch.object(vibebash_instance, 'execute_command', return_value=(True, "file1.txt\nfile2.txt")), \
             patch.object(vibebash_instance, 'save_to_history') as mock_save:
            
            await vibebash_instance.process_request("list files")
            
            # Verify command was saved to history
            mock_save.assert_called_once()
            saved_cmd = mock_save.call_args[0][0]
            assert saved_cmd.command == "ls -la"
            assert saved_cmd.success is True
    
    @pytest.mark.asyncio
    async def test_skip_command_workflow(self, vibebash_instance):
        """Test workflow with skipped commands"""
        mock_response = Mock()
        mock_response.content = json.dumps({
            "commands": [
                {
                    "command": "rm -rf /tmp/test",
                    "explanation": "Remove test directory", 
                    "risk_level": "high"
                }
            ]
        })
        
        with patch.object(vibebash_instance.llm, 'ainvoke', return_value=mock_response), \
             patch('vibebash.main.Prompt.ask', return_value='skip'), \
             patch.object(vibebash_instance, 'execute_command') as mock_exec:
            
            await vibebash_instance.process_request("remove test files")
            
            # Command should not be executed
            mock_exec.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_comment_and_regenerate_workflow(self, vibebash_instance):
        """Test workflow with user comments and regeneration"""
        # First LLM response
        mock_response1 = Mock()
        mock_response1.content = json.dumps({
            "commands": [
                {
                    "command": "ls",
                    "explanation": "List files",
                    "risk_level": "low"
                }
            ]
        })
        
        # Second LLM response after regeneration
        mock_response2 = Mock()
        mock_response2.content = json.dumps({
            "commands": [
                {
                    "command": "ls -la",
                    "explanation": "List all files with details",
                    "risk_level": "low"
                }
            ]
        })
        
        # Set up mock LLM for both responses
        setup_mock_llm_for_workflow(vibebash_instance, mock_response1)
        
        # Mock should handle multiple responses for regeneration
        from unittest.mock import AsyncMock
        vibebash_instance.llm.ainvoke = AsyncMock(side_effect=[mock_response1, mock_response2])
        
        user_inputs = ['comment', 'show more details', 'regenerate', 'run']
        
        with patch('vibebash.main.Prompt.ask', side_effect=user_inputs), \
             patch.object(vibebash_instance, 'execute_command', return_value=(True, "detailed output")):
            
            await vibebash_instance.process_request("list files")
            
            # Should have called ainvoke twice - initial and regeneration
            assert vibebash_instance.llm.ainvoke.call_count == 2
    
    @pytest.mark.asyncio
    async def test_quit_workflow(self, vibebash_instance):
        """Test workflow with quit action"""
        mock_response = Mock()
        mock_response.content = json.dumps({
            "commands": [
                {
                    "command": "sudo rm -rf /",
                    "explanation": "Dangerous command",
                    "risk_level": "high"
                }
            ]
        })
        
        with patch.object(vibebash_instance.llm, 'ainvoke', return_value=mock_response), \
             patch('vibebash.main.Prompt.ask', return_value='quit'), \
             patch.object(vibebash_instance, 'execute_command') as mock_exec:
            
            await vibebash_instance.process_request("dangerous request")
            
            # Command should not be executed
            mock_exec.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_failed_command_workflow(self, vibebash_instance):
        """Test workflow with failed command execution"""
        mock_response = Mock()
        mock_response.content = json.dumps({
            "commands": [
                {
                    "command": "invalid-command",
                    "explanation": "This command will fail",
                    "risk_level": "low"
                }
            ]
        })
        
        # Set up mock LLM
        setup_mock_llm_for_workflow(vibebash_instance, mock_response)
        
        with patch('vibebash.main.Prompt.ask', return_value='run'), \
             patch('vibebash.main.Confirm.ask', return_value=False), \
             patch.object(vibebash_instance, 'execute_command', return_value=(False, "command not found")), \
             patch.object(vibebash_instance, 'save_to_history') as mock_save:
            
            await vibebash_instance.process_request("run invalid command")
            
            # Failed command should still be saved to history
            mock_save.assert_called_once()
            saved_cmd = mock_save.call_args[0][0]
            assert saved_cmd.success is False
            assert "command not found" in saved_cmd.output
    
    @pytest.mark.asyncio
    async def test_multiple_commands_workflow(self, vibebash_instance):
        """Test workflow with multiple commands"""
        mock_response = Mock()
        mock_response.content = json.dumps({
            "commands": [
                {
                    "command": "pwd",
                    "explanation": "Show current directory",
                    "risk_level": "low"
                },
                {
                    "command": "ls -la",
                    "explanation": "List files with details",
                    "risk_level": "low"
                },
                {
                    "command": "df -h",
                    "explanation": "Show disk usage",
                    "risk_level": "low"
                }
            ]
        })
        
        user_inputs = ['run', 'skip', 'run']
        command_results = [
            (True, "/home/user"),
            (True, "total 8\nfile1.txt")
        ]
        
        # Set up mock LLM
        setup_mock_llm_for_workflow(vibebash_instance, mock_response)
        
        with patch('vibebash.main.Prompt.ask', side_effect=user_inputs), \
             patch.object(vibebash_instance, 'execute_command', side_effect=command_results), \
             patch.object(vibebash_instance, 'save_to_history') as mock_save:
            
            await vibebash_instance.process_request("show system info")
            
            # Should save 2 commands (run + run, skip doesn't save)
            assert mock_save.call_count == 2
    
    @pytest.mark.asyncio
    async def test_no_commands_generated(self, vibebash_instance):
        """Test workflow when no commands are generated"""
        with patch.object(vibebash_instance, 'get_commands', return_value=[]):
            await vibebash_instance.process_request("impossible request")
            
            # Should handle gracefully without errors
    
    @pytest.mark.asyncio
    async def test_llm_error_workflow(self, vibebash_instance):
        """Test workflow when LLM returns an error"""
        with patch.object(vibebash_instance.llm, 'ainvoke', side_effect=Exception("API Error")):
            await vibebash_instance.process_request("test request")
            
            # Should handle LLM errors gracefully


class TestWorkflowWithHistory:
    """Test workflows that use command history"""
    
    @pytest.mark.asyncio
    async def test_workflow_with_existing_history(self, vibebash_instance):
        """Test workflow that considers existing command history"""
        # Set up existing history
        vibebash_instance.history = [
            {
                "command": "cd /home/user",
                "timestamp": "2024-01-01T12:00:00",
                "success": True
            },
            {
                "command": "ls -la",
                "timestamp": "2024-01-01T12:01:00", 
                "success": True
            }
        ]
        
        mock_response = Mock()
        mock_response.content = json.dumps({
            "commands": [
                {
                    "command": "pwd",
                    "explanation": "Show current directory",
                    "risk_level": "low"
                }
            ]
        })
        
        with patch.object(vibebash_instance.llm, 'ainvoke', return_value=mock_response) as mock_llm, \
             patch('vibebash.main.Prompt.ask', return_value='run'), \
             patch.object(vibebash_instance, 'execute_command', return_value=(True, "/home/user")):
            
            await vibebash_instance.process_request("where am I")
            
            # Verify LLM was called with history context
            mock_llm.assert_called_once()
            call_args = mock_llm.call_args[0][0][0].content
            assert "cd /home/user" in call_args
            assert "ls -la" in call_args
"""
Unit tests for Pydantic models
"""
import pytest
from pydantic import ValidationError

from vibebash.main import Command, CommandList, ExecutedCommand


class TestCommand:
    """Test Command model"""
    
    def test_valid_command_creation(self):
        """Test creating a valid command"""
        cmd = Command(
            command="ls -la",
            explanation="List files with details",
            risk_level="low"
        )
        
        assert cmd.command == "ls -la"
        assert cmd.explanation == "List files with details"
        assert cmd.risk_level == "low"
    
    def test_command_serialization(self):
        """Test command JSON serialization"""
        cmd = Command(
            command="df -h",
            explanation="Show disk usage",
            risk_level="medium"
        )
        
        json_data = cmd.model_dump()
        assert json_data["command"] == "df -h"
        assert json_data["explanation"] == "Show disk usage"
        assert json_data["risk_level"] == "medium"
    
    def test_empty_command_fields(self):
        """Test command with empty required fields"""
        with pytest.raises(ValidationError):
            Command(command="", explanation="", risk_level="")


class TestCommandList:
    """Test CommandList model"""
    
    def test_valid_command_list(self, sample_commands):
        """Test creating a valid command list"""
        cmd_list = CommandList(commands=sample_commands)
        
        assert len(cmd_list.commands) == 3
        assert cmd_list.commands[0].command == "ls -la"
        assert cmd_list.commands[2].risk_level == "high"
    
    def test_empty_command_list(self):
        """Test empty command list should fail validation"""
        with pytest.raises(ValidationError):
            CommandList(commands=[])
    
    def test_command_list_serialization(self, sample_commands):
        """Test command list JSON serialization"""
        cmd_list = CommandList(commands=sample_commands[:2])
        json_data = cmd_list.model_dump()
        
        assert len(json_data["commands"]) == 2
        assert json_data["commands"][0]["command"] == "ls -la"


class TestExecutedCommand:
    """Test ExecutedCommand model"""
    
    def test_valid_executed_command(self):
        """Test creating a valid executed command"""
        exec_cmd = ExecutedCommand(
            command="ls -la",
            explanation="List files",
            timestamp="2024-01-01T12:00:00",
            success=True,
            output="total 8\ndrwxr-xr-x 2 user user 4096 Jan  1 12:00 ."
        )
        
        assert exec_cmd.command == "ls -la"
        assert exec_cmd.success is True
        assert exec_cmd.user_comment is None
    
    def test_executed_command_with_comment(self):
        """Test executed command with user comment"""
        exec_cmd = ExecutedCommand(
            command="df -h",
            explanation="Show disk usage",
            timestamp="2024-01-01T12:00:00",
            success=False,
            output="df: command not found",
            user_comment="This command should work on Linux"
        )
        
        assert exec_cmd.success is False
        assert exec_cmd.user_comment == "This command should work on Linux"
    
    def test_executed_command_dict_conversion(self):
        """Test executed command to dict conversion"""
        exec_cmd = ExecutedCommand(
            command="pwd",
            explanation="Print working directory",
            timestamp="2024-01-01T12:00:00",
            success=True,
            output="/home/user"
        )
        
        data = exec_cmd.model_dump()
        assert data["command"] == "pwd"
        assert data["success"] is True
        assert "user_comment" in data
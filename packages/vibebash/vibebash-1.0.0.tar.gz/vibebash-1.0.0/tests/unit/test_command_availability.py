"""
Tests for command availability checking
"""
from unittest.mock import patch, Mock
import pytest

from vibebash.main import VibeBash


@pytest.mark.ollama_only
class TestCommandAvailability:
    """Test command availability checking functionality"""
    
    def test_builtin_command_availability(self, vibebash_instance_ollama):
        """Test that built-in commands are considered available"""
        builtin_commands = ['ls', 'cd', 'pwd', 'echo', 'cat', 'grep']
        
        for cmd in builtin_commands:
            is_available, install_guide = vibebash_instance_ollama.check_command_availability(cmd)
            assert is_available is True
            assert install_guide == ""
    
    def test_available_command_with_shutil(self, vibebash_instance_ollama):
        """Test command that exists in PATH"""
        with patch('shutil.which', return_value='/usr/bin/python'):
            is_available, install_guide = vibebash_instance_ollama.check_command_availability('python')
            assert is_available is True
            assert install_guide == ""
    
    def test_unavailable_command(self, vibebash_instance_ollama):
        """Test command that doesn't exist"""
        with patch('shutil.which', return_value=None):
            is_available, install_guide = vibebash_instance_ollama.check_command_availability('nonexistent-command')
            assert is_available is False
            assert "not found" in install_guide
    
    def test_git_installation_guide_macos(self, vibebash_instance_ollama):
        """Test git installation guide for macOS"""
        with patch('shutil.which', return_value=None), \
             patch('platform.system', return_value='Darwin'):
            
            is_available, install_guide = vibebash_instance_ollama.check_command_availability('git')
            assert is_available is False
            assert "brew install git" in install_guide
    
    def test_git_installation_guide_linux(self, vibebash_instance_ollama):
        """Test git installation guide for Linux"""
        with patch('shutil.which', return_value=None), \
             patch('platform.system', return_value='Linux'):
            
            is_available, install_guide = vibebash_instance_ollama.check_command_availability('git')
            assert is_available is False
            assert "sudo apt install git" in install_guide
    
    def test_git_installation_guide_windows(self, vibebash_instance_ollama):
        """Test git installation guide for Windows"""
        with patch('shutil.which', return_value=None), \
             patch('platform.system', return_value='Windows'):
            
            is_available, install_guide = vibebash_instance_ollama.check_command_availability('git')
            assert is_available is False
            assert "winget install Git.Git" in install_guide
    
    def test_unknown_command_generic_guide(self, vibebash_instance_ollama):
        """Test generic installation guide for unknown commands"""
        with patch('shutil.which', return_value=None), \
             patch('platform.system', return_value='Darwin'):
            
            is_available, install_guide = vibebash_instance_ollama.check_command_availability('unknown-tool')
            assert is_available is False
            assert "brew install unknown-tool" in install_guide or "brew search unknown-tool" in install_guide
    
    def test_command_extraction_from_complex_command(self, vibebash_instance_ollama):
        """Test that main command is extracted from complex command strings"""
        with patch('shutil.which', return_value='/usr/bin/git'):
            # Test with arguments
            is_available, _ = vibebash_instance_ollama.check_command_availability('git status --porcelain')
            assert is_available is True
            
            # Test with pipes
            is_available, _ = vibebash_instance_ollama.check_command_availability('ls -la | grep test')
            assert is_available is True


@pytest.mark.ollama_only 
class TestCommandExecution:
    """Test command execution with availability checking"""
    
    def test_execute_available_command(self, vibebash_instance_ollama):
        """Test executing an available command"""
        with patch('shutil.which', return_value='/bin/echo'), \
             patch('subprocess.run') as mock_run:
            
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "hello world"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            success, output = vibebash_instance_ollama.execute_command('echo "hello world"')
            assert success is True
            assert output == "hello world"
    
    def test_execute_unavailable_command(self, vibebash_instance_ollama):
        """Test executing an unavailable command returns installation guide"""
        with patch('shutil.which', return_value=None), \
             patch('platform.system', return_value='Darwin'):
            
            success, output = vibebash_instance_ollama.execute_command('nonexistent-tool --help')
            assert success is False
            assert "not found" in output
            assert "brew" in output or "package manager" in output
    
    def test_execute_builtin_command_bypasses_check(self, vibebash_instance_ollama):
        """Test that builtin commands bypass availability check and execute normally"""
        with patch('subprocess.run') as mock_run:
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = "/home/user"
            mock_result.stderr = ""
            mock_run.return_value = mock_result
            
            success, output = vibebash_instance_ollama.execute_command('pwd')
            assert success is True
            mock_run.assert_called_once()
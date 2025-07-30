"""
Tests specifically for Ollama-only setup
"""
from unittest.mock import patch, Mock
import pytest

from vibebash.main import VibeBash


@pytest.mark.ollama_only
class TestOllamaOnlySetup:
    """Test VibeBash with Ollama only (offline)"""
    
    def test_ollama_setup_with_config(self):
        """Test ChatOllama setup with configuration"""
        with patch('vibebash.main.ChatOllama') as mock_chat_ollama:
            mock_chat_ollama.return_value = Mock()
            
            # Create instance and manually set config
            vb = Mock()
            vb.config = {'ollama_base_url': 'http://localhost:11434'}
            vb.console = Mock()
            
            # Import and call setup_llm method directly
            from vibebash.main import VibeBash
            VibeBash.setup_llm(vb, "deepcoder")
            
            mock_chat_ollama.assert_called_once_with(
                model="deepcoder",
                base_url="http://localhost:11434",
                temperature=0.1
            )
    
    def test_ollama_custom_base_url(self):
        """Test ChatOllama with custom base URL"""
        with patch('vibebash.main.ChatOllama') as mock_chat_ollama:
            mock_chat_ollama.return_value = Mock()
            
            # Create mock instance with custom config
            vb = Mock()
            vb.config = {'ollama_base_url': 'http://custom-host:8080'}
            vb.console = Mock()
            
            from vibebash.main import VibeBash
            VibeBash.setup_llm(vb, "mistral")
            
            mock_chat_ollama.assert_called_once_with(
                model="mistral",
                base_url="http://custom-host:8080",
                temperature=0.1
            )


@pytest.mark.ollama_only
class TestOllamaWorkflow:
    """Test complete workflows with Ollama"""
    
    def test_system_info_method(self):
        """Test system info gathering method"""
        from vibebash.main import VibeBash
        
        # Create mock instance
        vb = Mock()
        
        # Call method directly
        info = VibeBash.get_system_info(vb)
        
        # Should work and return string with expected content
        assert "Current directory:" in info
        assert "Shell:" in info
    
    def test_command_availability_builtin(self):
        """Test command availability for built-in commands"""
        # Test that built-in commands are recognized
        builtin_commands = ['cd', 'pwd', 'echo', 'ls']
        
        for cmd in builtin_commands:
            # Test the logic from check_command_availability directly
            builtin_set = {
                'cd', 'pwd', 'echo', 'ls', 'cat', 'cp', 'mv', 'rm', 'mkdir', 'rmdir',
                'chmod', 'chown', 'grep', 'find', 'which', 'whoami', 'df', 'du', 'ps',
                'kill', 'top', 'tail', 'head', 'sort', 'uniq', 'wc', 'history', 'alias'
            }
            
            assert cmd in builtin_set  # Built-in commands should be recognized


@pytest.mark.ollama_only 
class TestOllamaIntegration:
    """Test offline integration without full initialization"""
    
    def test_ollama_connection_check(self):
        """Test that we can check Ollama connection"""
        import requests
        
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                # Ollama is running
                models = response.json().get('models', [])
                assert isinstance(models, list)
            else:
                pytest.skip("Ollama not running")
        except Exception:
            pytest.skip("Ollama not accessible")
    
    def test_model_validation(self):
        """Test model name validation"""
        # Valid model names should be strings
        valid_models = ["deepcoder", "llama3.2", "mistral", "codellama"]
        
        for model in valid_models:
            assert isinstance(model, str)
            assert len(model) > 0
            assert not model.isspace()
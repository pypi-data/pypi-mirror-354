"""
Pytest configuration and shared fixtures
"""
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import pytest
from click.testing import CliRunner

from vibebash.main import VibeBash, Command, CommandList


def setup_mock_llm_for_workflow(vibebash_instance, mock_response):
    """Helper to set up mock LLM for workflow tests"""
    from unittest.mock import AsyncMock
    
    # Mock the streaming methods to avoid async issues
    vibebash_instance.llm.astream = None
    vibebash_instance.llm.stream = None
    vibebash_instance.llm.ainvoke = AsyncMock(return_value=mock_response)
    return vibebash_instance


@pytest.fixture
def temp_config_dir():
    """Create a temporary directory for config files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        with patch('pathlib.Path.home', return_value=temp_path):
            yield temp_path


@pytest.fixture
def mock_config_ollama():
    """Mock configuration data for Ollama only"""
    return {
        "ollama_base_url": "http://localhost:11434",
        "default_model_name": "llama3.2"
    }


@pytest.fixture
def mock_config():
    """Mock configuration data"""
    return {
        "ollama_base_url": "http://localhost:11434",
        "default_model_name": "llama3.2"
    }


@pytest.fixture
def sample_commands():
    """Sample command objects for testing"""
    return [
        Command(
            command="ls -la",
            explanation="List all files in current directory with details",
            risk_level="low"
        ),
        Command(
            command="df -h",
            explanation="Show disk usage in human readable format",
            risk_level="low"
        ),
        Command(
            command="sudo rm -rf /tmp/test",
            explanation="Remove test directory with force",
            risk_level="high"
        )
    ]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response"""
    class MockResponse:
        def __init__(self, content):
            self.content = content
    
    return MockResponse


@pytest.fixture
def cli_runner():
    """Click CLI test runner"""
    return CliRunner()


@pytest.fixture
def vibebash_instance_ollama(temp_config_dir, mock_config_ollama):
    """VibeBash instance with Ollama-only config"""
    config_file = temp_config_dir / ".vibebash_config.json"
    config_file.write_text(json.dumps(mock_config_ollama))
    
    with patch('vibebash.main.VibeBash.setup_llm'):
        vb = VibeBash()
        vb.config = mock_config_ollama
        vb.llm = Mock()  # Add mock llm attribute
        return vb


@pytest.fixture
def vibebash_instance(temp_config_dir, mock_config):
    """VibeBash instance with mocked config"""
    config_file = temp_config_dir / ".vibebash_config.json"
    config_file.write_text(json.dumps(mock_config))
    
    with patch('vibebash.main.VibeBash.setup_llm'):
        vb = VibeBash()
        vb.config = mock_config
        vb.llm = Mock()  # Add mock llm attribute
        return vb


@pytest.fixture
def mock_subprocess_success():
    """Mock successful subprocess execution"""
    mock_result = Mock()
    mock_result.returncode = 0
    mock_result.stdout = "Command executed successfully"
    mock_result.stderr = ""
    return mock_result


@pytest.fixture
def mock_subprocess_failure():
    """Mock failed subprocess execution"""
    mock_result = Mock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "Command failed"
    return mock_result


# Skip tests that require API keys if not available
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "requires_api_keys: mark test as requiring API keys"
    )
    config.addinivalue_line(
        "markers", "ollama_only: mark test as Ollama-only compatible"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to skip API key tests if keys not available"""
    import os
    
    skip_api_tests = pytest.mark.skip(reason="API keys not available")
    
    # Check if API keys are available
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
    
    for item in items:
        if "requires_api_keys" in item.keywords and not (has_openai or has_anthropic):
            item.add_marker(skip_api_tests)
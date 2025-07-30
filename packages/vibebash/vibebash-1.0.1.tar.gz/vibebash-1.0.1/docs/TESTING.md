# Testing Guide for VibeBash

This document provides comprehensive information about testing the VibeBash CLI tool.

## Table of Contents

- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Ollama-Only Testing](#ollama-only-testing)
- [Test Types](#test-types)
- [Writing Tests](#writing-tests)
- [Test Coverage](#test-coverage)
- [Mocking Guidelines](#mocking-guidelines)
- [CI/CD Integration](#cicd-integration)

## Test Structure

The test suite is organized into the following structure:

```
tests/
├── __init__.py                      # Test package initialization
├── conftest.py                     # Shared fixtures and configuration
├── pytest.ini                     # Pytest configuration
├── unit/                          # Unit tests
│   ├── test_models.py             # Pydantic model tests
│   ├── test_vibebash.py           # VibeBash class tests
│   ├── test_llm_setup.py          # LLM setup and configuration tests
│   ├── test_ollama_only.py        # Ollama-specific tests
│   └── test_command_availability.py # Command availability tests
├── integration/                   # Integration tests
│   ├── test_cli.py                # CLI command tests
│   └── test_full_workflow.py      # End-to-end workflow tests
├── fixtures/                     # Test data and fixtures
│   └── sample_responses.json     # Sample LLM responses
└── mocks/                        # Mock implementations
```

## Running Tests

### Prerequisites

Install test dependencies:

```bash
# Install with test dependencies
pip install -e ".[test]"

# Or install with all development dependencies
pip install -e ".[dev]"
```

### Basic Test Execution

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_models.py

# Run specific test class
pytest tests/unit/test_models.py::TestCommand

# Run specific test method
pytest tests/unit/test_models.py::TestCommand::test_valid_command_creation
```

## Ollama-Only Testing

**🚀 NEW: Test without API Keys!**

If you don't have OpenAI or Anthropic API keys, you can still run comprehensive tests using our Ollama-only test suite:

### Quick Start

```bash
# Run Ollama-only tests (no API keys required)
make test-ollama

# Or run directly
python run_ollama_tests.py
```

### What Gets Tested

The Ollama-only test suite includes:
- ✅ All Pydantic model validation
- ✅ Core VibeBash functionality  
- ✅ Command availability checking
- ✅ Installation guidance system
- ✅ Error handling and feedback
- ✅ CLI interface (mocked)
- ✅ Configuration management

### Prerequisites for Ollama Testing

1. **Install Ollama** (optional - tests work with mocks):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve
   
   # Pull a model (optional)
   ollama pull llama2
   ```

2. **Install test dependencies**:
   ```bash
   pip install -e ".[test]"
   ```

### Test Categories

Run tests by category using markers:

```bash
# Run only Ollama-compatible tests
pytest -m ollama_only

# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip tests that require API keys
pytest -m "not requires_api_keys"
```

### Coverage Reports

```bash
# Run tests with coverage
pytest --cov=vibebash

# Generate HTML coverage report for Ollama tests
pytest tests/unit/test_ollama_only.py tests/unit/test_command_availability.py --cov=vibebash --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Types

### Unit Tests

Unit tests focus on testing individual components in isolation:

- **Model Tests** (`test_models.py`): Test Pydantic models for validation and serialization
- **Core Logic Tests** (`test_vibebash.py`): Test VibeBash class methods
- **LLM Setup Tests** (`test_llm_setup.py`): Test provider configuration
- **Ollama Tests** (`test_ollama_only.py`): Test Ollama-specific functionality
- **Command Availability** (`test_command_availability.py`): Test command checking and installation guides

### Integration Tests

Integration tests verify component interactions:

- **CLI Tests** (`test_cli.py`): Test command-line interface
- **Workflow Tests** (`test_full_workflow.py`): Test complete user workflows

## Writing Tests

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`
- Use descriptive names that explain what is being tested

```python
def test_execute_successful_command_returns_true_and_output():
    """Test that executing a successful command returns True and command output"""
```

### Using Fixtures

Common fixtures are defined in `conftest.py`:

```python
def test_command_execution(vibebash_instance_ollama, mock_subprocess_success):
    """Test using Ollama-compatible fixtures"""
    with patch('subprocess.run', return_value=mock_subprocess_success):
        success, output = vibebash_instance_ollama.execute_command("ls -la")
        assert success is True
```

### Async Test Examples

For testing async functionality:

```python
@pytest.mark.asyncio
async def test_async_command_processing(vibebash_instance_ollama):
    """Test async command processing with Ollama"""
    with patch.object(vibebash_instance_ollama.llm, 'invoke') as mock_llm:
        mock_llm.return_value = mock_response
        await vibebash_instance_ollama.process_request("test request")
        mock_llm.assert_called_once()
```

### Testing New Features

When testing command availability and error feedback:

```python
@pytest.mark.ollama_only
def test_command_availability_checking(vibebash_instance_ollama):
    """Test command availability with installation guidance"""
    with patch('shutil.which', return_value=None):
        is_available, guide = vibebash_instance_ollama.check_command_availability('git')
        assert is_available is False
        assert "install" in guide.lower()
```

## Test Coverage

### Coverage Goals

- **Minimum**: 80% overall coverage
- **Target**: 90%+ coverage for core functionality
- **Critical paths**: 100% coverage for safety-critical code

### New Feature Coverage

Recent additions achieve high coverage:
- ✅ Command availability checking: 95%+
- ✅ Installation guidance: 90%+
- ✅ Error feedback to AI: 85%+
- ✅ Ollama-only setup: 90%+

## API Key Management

### Test Configuration

The test suite automatically handles API key availability:

```python
# Tests marked with @pytest.mark.requires_api_keys are skipped if no keys available
@pytest.mark.requires_api_keys
def test_openai_integration():
    """This test only runs if OPENAI_API_KEY is available"""
    pass

# Tests marked with @pytest.mark.ollama_only always run
@pytest.mark.ollama_only  
def test_ollama_functionality():
    """This test runs without any API keys"""
    pass
```

### Environment Variables

```bash
# Optional: Set API keys for full testing
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Tests automatically detect and use available keys
pytest

# Force Ollama-only testing (ignore any API keys)
export SKIP_API_TESTS=1
pytest
```

## Mocking Guidelines

### External Dependencies

Mock external dependencies to ensure test isolation:

```python
# Mock LLM API calls
with patch.object(vibebash_instance_ollama.llm, 'invoke', return_value=mock_response):
    # Test code here

# Mock subprocess execution
with patch('subprocess.run', return_value=mock_result):
    # Test code here

# Mock command availability
with patch('shutil.which', return_value=None):
    # Test command not found scenario
```

### Command Availability Testing

```python
# Test different operating systems
with patch('platform.system', return_value='Darwin'):
    guide = vb.get_installation_guide('git')
    assert 'brew install git' in guide

with patch('platform.system', return_value='Linux'):
    guide = vb.get_installation_guide('git') 
    assert 'sudo apt install git' in guide
```

## Test Data Management

### Using Fixtures

Test data is stored in `tests/fixtures/`:

```python
@pytest.fixture
def sample_llm_response():
    """Load sample LLM response from fixtures"""
    with open('tests/fixtures/sample_responses.json') as f:
        return json.load(f)
```

### Command Availability Test Data

Built-in commands are automatically tested:

```python
builtin_commands = ['ls', 'cd', 'pwd', 'echo', 'cat', 'grep']
for cmd in builtin_commands:
    is_available, guide = vb.check_command_availability(cmd)
    assert is_available is True
```

## Debugging Tests

### Running Tests in Debug Mode

```bash
# Run with pdb on failure
pytest --pdb

# Run Ollama tests with maximum verbosity
python run_ollama_tests.py

# Run specific test with output
pytest -vv -s tests/unit/test_command_availability.py::TestCommandAvailability::test_git_installation_guide_macos
```

## Continuous Integration

### GitHub Actions

Tests run automatically with different configurations:
- Full test suite (with API keys)
- Ollama-only test suite (no API keys)
- Multi-platform testing (Linux, macOS, Windows)

### Local CI Simulation

```bash
# Simulate CI environment locally
make ci-test

# Test without API keys (like CI might)
unset OPENAI_API_KEY ANTHROPIC_API_KEY
make test-ollama
```

## Best Practices

### Test Independence

- Each test should be independent
- Use fixtures for setup/teardown
- Clean up resources after tests
- Mock external dependencies

### Ollama-Only Testing

- Use `@pytest.mark.ollama_only` for compatible tests
- Use `vibebash_instance_ollama` fixture
- Mock API calls when needed
- Test core functionality without external dependencies

### Error Testing

- Test both success and failure paths
- Verify error messages and types  
- Test edge cases and boundary conditions
- Test command availability scenarios

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure package is installed in development mode
pip install -e .
```

**Ollama Connection Issues:**
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve
```

**Missing Dependencies:**
```bash
# Install test dependencies
pip install -e ".[test]"
```

### Running Ollama Tests

If you encounter issues with Ollama testing:

1. **Check Python environment**:
   ```bash
   python --version  # Should be 3.8+
   pip list | grep pytest
   ```

2. **Run test subset**:
   ```bash
   # Run just model tests
   pytest tests/unit/test_models.py -v
   
   # Run just availability tests  
   pytest tests/unit/test_command_availability.py -v
   ```

3. **Check test markers**:
   ```bash
   # List all available test markers
   pytest --markers
   
   # Run only Ollama-compatible tests
   pytest -m ollama_only -v
   ```

For more help, see the [project documentation](../README.md) or open an issue on GitHub.

## Quick Reference

### Most Useful Commands

```bash
# 🚀 Test without API keys
make test-ollama

# 📊 Full test with coverage
make coverage  

# 🔍 Test specific functionality
pytest tests/unit/test_command_availability.py -v

# 🐛 Debug failing test
pytest tests/unit/test_models.py::TestCommand::test_valid_command_creation --pdb

# ⚡ Quick development test
make quick-test
```
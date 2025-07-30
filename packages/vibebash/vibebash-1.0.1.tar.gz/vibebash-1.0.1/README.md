# VibeBash - Offline AI Shell Assistant

**VibeBash** is a completely offline natural language to shell command translator powered by local AI models through Ollama. No API keys, no internet connection required - everything runs locally on your machine.

## 🌟 Features

- **🔒 100% Offline**: All processing happens locally via Ollama
- **🤖 AI-Powered**: Convert natural language to shell commands
- **🚀 Fast**: Local models mean no network latency
- **🔐 Private**: Your commands never leave your machine
- **🎯 Accurate**: Supports reasoning models like deepcoder
- **⚡ Interactive**: Review, modify, or skip commands before execution
- **📝 Smart History**: Learn from previous command patterns
- **🛠️ Command Validation**: Checks command availability and provides installation hints

## 🎯 Supported Models

VibeBash works with any Ollama-compatible model:

- **deepcoder** - Reasoning model with think tokens (recommended)
- **llama3.2** - Fast and capable general model
- **codellama** - Code-focused model
- **mistral** - Efficient and accurate
- **gemma** - Google's lightweight model

## 📦 Installation

### Requirements

1. **Python 3.8+**
2. **Ollama** - [Install from ollama.ai](https://ollama.ai)

### Quick Install with pipx (Recommended)

```bash
pipx install vibebash
```

### Install from Source

```bash
git clone https://github.com/yourusername/vibebash.git
cd vibebash
pip install -e .
```

### Development Setup

```bash
./scripts/setup-dev.sh
```

## 🚀 Quick Start

1. **Start Ollama**:
   ```bash
   ollama serve
   ```

2. **Pull a model** (if you don't have one):
   ```bash
   ollama pull deepcoder    # Reasoning model (recommended)
   # or
   ollama pull llama3.2     # Fast general model
   ```

3. **Run VibeBash**:
   ```bash
   vibebash "list all Python files in this directory"
   ```

4. **First time setup** - VibeBash will ask for:
   - Ollama base URL (default: http://localhost:11434)
   - Default model name (e.g., deepcoder, llama3.2)

## 💡 Usage Examples

### Basic Commands
```bash
vibebash "show disk usage"
vibebash "find large files over 100MB"
vibebash "kill process on port 8080"
```

### With Specific Models
```bash
vibebash --model-name deepcoder "optimize this Python script"
vibebash --model-name llama3.2 "compress all images in this folder"
```

### Interactive Mode
```bash
vibebash
# Then type your request when prompted
```

### View History
```bash
vibebash --history
```

### Reconfigure
```bash
vibebash --config
```

## 🔧 Configuration

VibeBash stores configuration in `~/.vibebash_config.json`:

```json
{
  "ollama_base_url": "http://localhost:11434",
  "default_model_name": "deepcoder"
}
```

### Custom Ollama Setup

If running Ollama on a different host or port:

```bash
vibebash --config
# Enter custom URL like: http://my-server:11434
```

## 🧪 Testing

### Run All Tests
```bash
make test-ollama
```

### Quick Core Tests
```bash
python3 -m pytest tests/unit/test_models.py tests/unit/test_command_availability.py -v
```

### Test with Your Model
```bash
make test-deepcoder  # Test with deepcoder model
```

## 📁 Project Structure

```
vibebash/
├── vibebash/           # Main package
│   ├── main.py         # Core VibeBash class
│   └── __init__.py     # Package initialization
├── tests/              # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── scripts/            # Setup and utility scripts
│   ├── quick-start.sh  # Quick setup
│   └── setup-dev.sh    # Development setup
└── docs/               # Documentation
```

## 🛠️ Development

### Setup Development Environment
```bash
./scripts/setup-dev.sh
```

### Run Tests
```bash
make test           # All tests
make test-unit      # Unit tests only
make coverage       # With coverage report
```

### Code Quality
```bash
make lint           # Linting
make format         # Code formatting
make type-check     # Type checking
```

### Build Package
```bash
make build
```

## 🤖 Model Recommendations

### For Reasoning Tasks (Recommended)
- **deepcoder**: Best for complex command generation with step-by-step thinking
- **codellama**: Good for code-related tasks

### For Speed
- **llama3.2**: Fast and lightweight, good balance of speed and accuracy
- **gemma**: Very fast, good for simple commands

### Memory Usage
- **Small models**: llama3.2 (3B), gemma (2B-7B)
- **Large models**: deepcoder (14B), codellama (13B+)

## 🔍 How It Works

1. **Input**: You provide a natural language description
2. **Processing**: Local Ollama model converts it to shell commands  
3. **Validation**: VibeBash checks command availability
4. **Review**: You can approve, modify, or skip each command
5. **Execution**: Commands run in your local shell
6. **Learning**: History helps improve future suggestions

## 🛡️ Privacy & Security

- **No Data Transmission**: Everything stays on your machine
- **No API Keys**: No external services required
- **Command Review**: You control what gets executed
- **Safe Defaults**: Built-in protections against dangerous commands

## 📚 Advanced Usage

### Custom Prompts
VibeBash includes system context about your environment:
- Current directory
- Available commands
- Operating system
- Recent command history

### Batch Operations
```bash
vibebash "create backup of all config files and compress them"
vibebash "find and remove all temporary files older than 7 days"
```

### Error Recovery
When commands fail, VibeBash can suggest alternatives:
```bash
vibebash "install package X"
# If package manager not found, suggests alternatives for your OS
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `make test-ollama`
4. Submit a pull request

## 📜 License

MIT License - see [LICENSE](LICENSE) file.

## 🔗 Links

- **Ollama**: https://ollama.ai
- **Models**: https://ollama.ai/library
- **Issues**: https://github.com/yourusername/vibebash/issues

---

**VibeBash**: Because your shell should understand you, not the other way around. 🎯
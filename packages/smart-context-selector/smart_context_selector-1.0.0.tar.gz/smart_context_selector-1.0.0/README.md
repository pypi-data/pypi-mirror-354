# 🎯 Smart Context Selector

Intelligently selects and bundles documentation for optimal AI assistant context. Originally built for n8n workflows, but extensible to any documentation set.

## 🌟 Features

- **Intelligent Analysis**: Analyzes your prompts to detect required services and concepts
- **Smart Selection**: Uses relevance scoring to select the most important documentation
- **Context Optimization**: Stays within AI context limits (85-95% usage)
- **Multiple Configs**: Built-in configurations for different platforms
- **CLI & Python API**: Use from command line or import as a library

## 🚀 Quick Start

### Installation

```bash
pip install smart-context-selector
```

### Command Line Usage

```bash
# Basic usage with built-in n8n config
smart-context --prompt "build a slack bot with AI" --config n8n

# Custom bundle name
smart-context --prompt "create API integration" --name my_integration

# List available configurations
smart-context --list-configs

# Use custom configuration file
smart-context --prompt "build react app" --config-file my_docs.json
```

### Python API Usage

```python
from smart_context_selector import SmartContextSelector

# Initialize with built-in config
selector = SmartContextSelector(config_name="n8n")

# Or with custom config
selector = SmartContextSelector(config_file="my_config.json")

# Create context bundle
bundle_path = selector.create_context_bundle(
    prompt="Create an AI chatbot that monitors Slack",
    bundle_name="slack_ai_bot"
)

print(f"Bundle created at: {bundle_path}")
```

## 📁 Configuration

### Built-in Configurations

- **n8n**: Complete n8n workflow automation documentation
- More configurations coming soon!

### Custom Configuration Format

Create a JSON file with this structure:

```json
{
  "name": "my_platform",
  "description": "My Platform Documentation",
  "docs_dir": "path/to/docs",
  "knowledge_base": {
    "keyword": ["folder1", "folder2"],
    "api": ["integrations", "reference"],
    "database": ["data", "storage"]
  },
  "file_patterns": {
    "core_always": ["getting-started", "basics"],
    "api_specific": ["auth", "endpoints"],
    "advanced": ["deployment", "scaling"]
  }
}
```

## 🎯 How It Works

1. **Prompt Analysis**: Analyzes your prompt to identify key concepts and services
2. **Relevance Scoring**: Scores documentation files based on detected concepts
3. **Smart Selection**: Selects the most relevant files within context limits
4. **Bundle Creation**: Creates an optimized documentation bundle
5. **Ready for AI**: Upload the bundle to your AI assistant for optimal context

## 📊 Example Output

```
🔍 Analyzing prompt: Create an AI chatbot that monitors Slack...

📊 Analysis Results:
  🎯 Workflow Type: ai_focused
  🔧 Detected Services: ai, slack, chatbot, webhook
  📁 Required Folders: ai_langchain, nodes_integrations, workflows
  📈 Complexity Score: 4

📋 Selected 85 files for optimal AI context

✅ Created bundle: slack_ai_bot
📁 Location: smart_context_bundles/slack_ai_bot
📄 Files: 85
```

## 🛠️ CLI Options

```bash
smart-context [OPTIONS]

Options:
  --prompt, -p TEXT          Prompt describing what you want to build [required]
  --config, -c TEXT          Built-in configuration to use (default: n8n)
  --config-file TEXT         Path to custom configuration JSON file
  --name, -n TEXT            Custom bundle name
  --docs-dir TEXT            Override documentation directory from config
  --max-files INTEGER        Maximum number of files to include (default: 120)
  --push                     Push bundle to GitHub after creation
  --list-configs             List available built-in configurations
  --version                  Show version
  --help                     Show this message and exit
```

## 🧪 Development

### Setup Development Environment

```bash
git clone https://github.com/yourusername/smart-context-selector.git
cd smart-context-selector
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/smart-context-selector/issues)
- **Documentation**: [Full Documentation](https://github.com/yourusername/smart-context-selector)

## 🙏 Acknowledgments

Originally developed for n8n workflow automation documentation bundling.

---

**Made with ❤️ for the AI development community**
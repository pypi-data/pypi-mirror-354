# Triksha - Advanced LLM Security Testing Framework

Triksha is a comprehensive framework for testing and evaluating Large Language Models (LLMs) for security vulnerabilities, including jailbreaking, prompt injection, and harmful content generation.

## Features

- **Static Red Teaming**: Test models with predefined adversarial prompts to evaluate resilience to jailbreaking
- **Scheduled Red Teaming**: Schedule automated red teaming runs at specified intervals to continuously monitor model safety
- **Conversation Red Teaming**: Simulate multi-turn conversations to test for more complex vulnerabilities
- **Comprehensive Metrics**: Track success rates, response times, and vulnerability patterns
- **Email Notifications**: Get notified when benchmarks complete with detailed results
- **Custom API Models**: Test your own API endpoints with flexible configuration
- **Guardrail Testing**: Evaluate safety guardrails and content filtering systems
- **Multi-Model Benchmarking**: Compare performance across different model providers

## Requirements

- Python 3.8+
- API keys for the models you want to test (OpenAI, Google, Anthropic, etc.)

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install triksha
```

### Option 2: Install from Source

```bash
# Clone the repository
git clone https://github.com/triksha-ai/triksha.git
cd triksha

# Install in development mode
pip install -e .
```

## Quick Start

After installation, you can start using Triksha immediately:

```bash
# Launch the interactive CLI
triksha

# Or use the alternative command
triksha-cli
```

## Usage

### Static Red Teaming

Run the static red teaming benchmark:

```bash
triksha
# Then select "Perform Red Teaming" from the menu
```

This will guide you through selecting models, techniques, and other parameters for testing.

### Scheduled Red Teaming

Scheduled benchmarks allow you to run red teaming tests automatically at specified intervals.

1. Launch Triksha and navigate to "Schedule Red Teaming"
2. Configure your benchmark parameters
3. Set the schedule interval
4. The scheduler will run automatically in the background

### Email Notifications

Configure email notifications to get results when benchmarks complete:

1. Launch Triksha
2. Go to "Settings" → "Configure Email Notifications"
3. Enter your Gmail credentials and notification preferences

### Environment Variables

Create a `.env` file in your working directory or set these environment variables:

```bash
# Required API keys (set only the ones you need)
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Optional: Email notifications
GMAIL_USER=your_email@gmail.com
GMAIL_PASSWORD=your_app_password

# Optional: Custom model configurations
CUSTOM_MODEL_CONFIG_PATH=/path/to/your/models
```

## API Keys Setup

Triksha supports multiple model providers. You only need to set up API keys for the providers you want to use:

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Anthropic**: Get your API key from [Anthropic Console](https://console.anthropic.com/)

## Documentation

- [Scheduled Benchmarks](docs/scheduled_benchmarks.md)
- [API Reference](docs/api.md)
- [Benchmark Types](docs/benchmarks.md)
- [Custom Models](docs/custom_models.md)
- [Guardrail Testing](docs/guardrails.md)

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

[MIT License](LICENSE)

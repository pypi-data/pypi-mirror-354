# 🔥 Keyforge

Test API keys for multiple LLM providers with confidence.

## Features

- **Config-driven**: Provider URLs and settings in JSON
- **CLI arguments**: Test specific models or providers
- **Multi-provider**: Supports 6+ LLM providers out of the box
- **UV optimized**: Fast dependency management

## Installation

```bash
git clone <repository-url>
cd keyforge

# Install dependencies
uv sync
# or: pip install -r requirements.txt

# Setup environment
cp .env.sample .env
# Edit .env with your actual API keys
```

## Usage

### Development (Local)
```bash
# Test all models
uv run keyforge.py

# Test specific model
uv run keyforge.py model1

# Test multiple models  
uv run keyforge.py model1 model3

# Test by provider
uv run keyforge.py --provider anthropic

# List available models
uv run keyforge.py --list

# Show help
uv run keyforge.py --help
```

### Installed Package
```bash
# Install globally
pip install keyforge

# Use the CLI command
keyforge model1
keyforge --provider anthropic
keyforge --list
```

## Configuration

### API Keys (`.env`)
```env
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
XAI_API_KEY=your_key_here
```

### Models (`config.json`)
```json
{
  "providers": {
    "anthropic": {
      "url": "https://api.anthropic.com/v1/messages",
      "apiKeyEnv": "ANTHROPIC_API_KEY",
      "authHeader": "x-api-key"
    }
  },
  "models": {
    "model1": {
      "provider": "anthropic",
      "modelId": "claude-sonnet-4-20250514",
      "maxTokens": 1000,
      "temperature": 0.2
    }
  }
}
```

## Supported Providers

- **Anthropic** - Claude models
- **OpenAI** - GPT and O-series models  
- **Google** - Gemini models
- **Perplexity** - Search-enhanced AI
- **OpenRouter** - Multi-model aggregator
- **XAI** - Grok models

## Adding New Providers

Add to the `providers` section in `config.json`:

```json
"newprovider": {
  "url": "https://api.example.com/v1/chat",
  "apiKeyEnv": "NEW_PROVIDER_API_KEY",
  "headers": {"Content-Type": "application/json"},
  "authHeader": "Authorization",
  "authPrefix": "Bearer ",
  "responseField": "choices[0].message.content"
}
```

## Security

⚠️ **Never commit `.env` files to version control**

- ✅ `.env.sample` - Safe template with placeholders
- ❌ `.env` - Contains actual API keys (git-ignored)

## Files

| File | Description | Safe to Share |
|------|-------------|---------------|
| `keyforge.py` | Main script | ✅ |
| `config.json` | Configuration | ✅ |
| `.env.sample` | Key template | ✅ |
| `.env` | **Actual keys** | ❌ |

## Dependencies

- `requests` - HTTP client
- `python-dotenv` - Environment variables
- Python 3.8+

## License

MIT

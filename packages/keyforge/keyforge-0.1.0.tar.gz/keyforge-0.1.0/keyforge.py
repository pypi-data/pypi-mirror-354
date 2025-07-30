#!/usr/bin/env python3
"""
Keyforge - Test API keys for multiple LLM providers
A config-driven tool for testing LLM API keys across various providers
"""

import os
import json
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_nested_value(data, path):
    """Get value from nested dict using dot notation (e.g., 'content[0].text')"""
    try:
        # Handle array notation
        if '[' in path and ']' in path:
            parts = path.replace('[', '.').replace(']', '').split('.')
            result = data
            for part in parts:
                if part.isdigit():
                    result = result[int(part)]
                elif part:
                    result = result[part]
            return result
        else:
            # Simple dot notation
            parts = path.split('.')
            result = data
            for part in parts:
                result = result[part]
            return result
    except (KeyError, IndexError, TypeError):
        return None

def test_provider(provider_config, model_id, prompt, max_tokens, temperature):
    """Generic provider testing function"""
    
    # Get API key
    api_key_env = provider_config.get('apiKeyEnv')
    api_key = os.getenv(api_key_env)
    
    if not api_key or api_key.startswith('YOUR_'):
        return False, f"No valid API key found for {api_key_env}"
    
    # Build headers
    headers = provider_config.get('headers', {}).copy()
    auth_header = provider_config.get('authHeader')
    auth_prefix = provider_config.get('authPrefix', '')
    
    if auth_header:
        headers[auth_header] = f"{auth_prefix}{api_key}"
    
    # Build request data
    data = {
        'model': model_id,
        'max_tokens': min(max_tokens, 4096),  # Safety limit
        'messages': [
            {'role': 'system', 'content': prompt['system']},
            {'role': 'user', 'content': prompt['user']}
        ],
        'temperature': temperature
    }
    
    try:
        url = provider_config.get('url')
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            response_field = provider_config.get('responseField', 'content')
            content = get_nested_value(result, response_field)
            
            if content:
                return True, str(content)[:100]
            else:
                return False, f"No content found in response field: {response_field}"
        else:
            return False, f"HTTP {response.status_code}: {response.text[:200]}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main testing function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Keyforge - Test API keys for multiple LLM providers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  # Development usage
  uv run keyforge.py                    # Test all models
  uv run keyforge.py model1             # Test only model1
  uv run keyforge.py model1 model3      # Test model1 and model3
  uv run keyforge.py --provider openai  # Test all OpenAI models
  uv run keyforge.py --list             # List available models
  
  # Installed usage
  keyforge                               # Test all models
  keyforge model1                        # Test only model1
  keyforge --provider anthropic          # Test all Anthropic models
  keyforge --list                        # List available models"""
    )
    
    parser.add_argument('models', nargs='*', help='Specific model names to test (e.g., model1 model2)')
    parser.add_argument('--provider', '-p', help='Test all models from a specific provider')
    parser.add_argument('--list', '-l', action='store_true', help='List available models and exit')
    
    args = parser.parse_args()
    
    print("KEYFORGE - Multi-Provider LLM Key Tester")
    print("=" * 50)
    
    # Load config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load config.json: {e}")
        return
    
    providers = config.get('providers', {})
    models = config.get('models', {})
    prompt = config.get('prompt', {})
    
    if not providers:
        print("ERROR: No providers found in config.json")
        return
        
    if not models:
        print("ERROR: No models found in config.json")
        return
    
    # Handle --list option
    if args.list:
        print("\nAVAILABLE MODELS:")
        for model_name, model_config in models.items():
            provider = model_config.get('provider')
            model_id = model_config.get('modelId')
            print(f"  {model_name:<12} -> {provider}/{model_id}")
        print(f"\nAVAILABLE PROVIDERS: {', '.join(providers.keys())}")
        return
    
    # Filter models based on arguments
    models_to_test = {}
    
    if args.provider:
        # Test all models from specific provider
        if args.provider not in providers:
            print(f"ERROR: Provider '{args.provider}' not found. Available: {', '.join(providers.keys())}")
            return
        
        models_to_test = {name: config for name, config in models.items() 
                         if config.get('provider') == args.provider}
        
        if not models_to_test:
            print(f"ERROR: No models found for provider '{args.provider}'")
            return
            
        print(f"TESTING models from provider: {args.provider}")
        
    elif args.models:
        # Test specific models
        for model_name in args.models:
            if model_name in models:
                models_to_test[model_name] = models[model_name]
            else:
                print(f"ERROR: Model '{model_name}' not found. Available: {', '.join(models.keys())}")
                return
        
        print(f"TESTING specific models: {', '.join(args.models)}")
        
    else:
        # Test all models (default behavior)
        models_to_test = models
        print("TESTING all models")
    
    # Test each selected model
    for model_name, model_config in models_to_test.items():
        provider_name = model_config.get('provider')
        model_id = model_config.get('modelId')
        max_tokens = model_config.get('maxTokens', 1000)
        temperature = model_config.get('temperature', 0.7)
        
        print(f"\nTesting {model_name} ({provider_name}/{model_id})")
        
        if provider_name not in providers:
            print(f"ERROR: Provider '{provider_name}' not found in config")
            continue
        
        provider_config = providers[provider_name]
        success, result = test_provider(provider_config, model_id, prompt, max_tokens, temperature)
        
        if success:
            print(f"SUCCESS: {result}...")
        else:
            print(f"FAILED: {result}")
    
    print("\n" + "=" * 50)
    print("KEYFORGE testing complete!")

if __name__ == "__main__":
    main()

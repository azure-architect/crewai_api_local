#!/usr/bin/env python3
"""
Test script for the Ollama LLM Client.
This script tests basic functionality of the client:
- Connecting to Ollama
- Listing available models
- Generating a model config file
- Text generation with the default model
- Getting embeddings
"""

import sys
import os
from pathlib import Path

# Add the parent directory to the path so we can import our module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the OllamaClient from the correct location
try:
    from crew.interfaces.ollama_llm_client import OllamaClient
    print("Successfully imported OllamaClient")
except ImportError as e:
    print(f"Error: Could not import OllamaClient. Make sure the module path is correct. Details: {e}")
    sys.exit(1)

def test_ollama_client():
    """Test basic functionality of the OllamaClient."""
    print("="*50)
    print("Testing Ollama LLM Client")
    print("="*50)
    
    # Step 1: Create client and test connection
    print("\n1. Creating Ollama client and testing connection...")
    client = OllamaClient()
    
    # Step 2: List available models
    print("\n2. Listing available models...")
    models = client.list_models()
    
    if not models:
        print("Error: No models found. Is Ollama running?")
        return False
    
    print(f"Found {len(models)} models:")
    for i, model in enumerate(models[:5], 1):  # Show first 5 models
        print(f"  {i}. {model['name']}")
    
    if len(models) > 5:
        print(f"  ... and {len(models) - 5} more")
    
    # Step 3: Generate models config
    print("\n3. Generating models config file...")
    config_path = "test_models_config.yaml"
    config = client.export_models_config(config_path)
    
    if os.path.exists(config_path):
        print(f"Successfully generated config at {config_path}")
        
        # Show default models selected
        print(f"Default generation model: {config['default_generation_model']}")
        print(f"Default embedding model: {config['default_embedding_model']}")
    else:
        print(f"Error: Failed to generate config at {config_path}")
    
    # Step 4: Test text generation
    print("\n4. Testing text generation...")
    prompt = "Explain what a mixture of experts model is in one sentence:"
    print(f"Prompt: {prompt}")
    
    response = client.generate(prompt, options={"temperature": 0.3})
    print(f"Response: {response}")
    
    # Step 5: Test embeddings
    print("\n5. Testing embeddings generation...")
    text = "This is a test of the embedding functionality."
    print(f"Text: {text}")
    
    embedding = client.get_embeddings(text)
    if embedding:
        print(f"Successfully generated embedding with {len(embedding)} dimensions")
        # Show a few values from the embedding
        print(f"First 5 values: {embedding[:5]}")
    else:
        print("Error: Failed to generate embedding")
    
    print("\nAll tests completed!")
    return True

if __name__ == "__main__":
    success = test_ollama_client()
    sys.exit(0 if success else 1)
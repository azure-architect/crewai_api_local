import requests
import json
import yaml
import os
from typing import Dict, Any, Optional, List, Union
from pathlib import Path

class OllamaClient:
    """Client for interacting with Ollama API to run local LLMs."""
    
    def __init__(
        self, 
        base_url: str = "http://localhost:11434",
        model: str = "llama3:8b-instruct-fp16",
        embedding_model: str = "nomic-embed-text",
        temperature: float = 0.7,
        config_path: Optional[str] = None,
        auto_detect_models: bool = True
    ):
        """
        Initialize the Ollama client.
        
        Args:
            base_url: Base URL for the Ollama API
            model: Default model name to use for generation
            embedding_model: Model to use for embeddings
            temperature: Temperature for generation (0.0 to 1.0)
            config_path: Path to YAML config file (optional)
            auto_detect_models: Whether to automatically detect available models
        """
        # Load config if provided
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                base_url = config.get('ollama_url', base_url)
                model = config.get('ollama_generation_model', model)
                embedding_model = config.get('ollama_embedding_model', embedding_model)
                temperature = config.get('temperature', temperature)
        
        self.base_url = base_url
        self.model = model
        self.embedding_model = embedding_model
        self.temperature = temperature
        self.generate_endpoint = f"{base_url}/api/generate"
        self.embedding_endpoint = f"{base_url}/api/embeddings"
        self.models_endpoint = f"{base_url}/api/tags"
        
        # Store available models
        self.available_models = []
        if auto_detect_models:
            self.refresh_available_models()
    
    def refresh_available_models(self) -> List[Dict[str, Any]]:
        """
        Refresh the list of available models from the Ollama instance.
        
        Returns:
            List of available models
        """
        self.available_models = self.list_models()
        return self.available_models
    
    def list_models(self) -> List[Dict[str, Any]]:
        """
        Get a list of available models from the Ollama instance.
        
        Returns:
            List of model information dictionaries
        """
        try:
            response = requests.get(self.models_endpoint)
            response.raise_for_status()
            result = response.json()
            return result.get("models", [])
        except Exception as e:
            print(f"Error getting model list: {e}")
            return []
    
    def is_model_available(self, model_name: str) -> bool:
        """
        Check if a specific model is available.
        
        Args:
            model_name: The name of the model to check
            
        Returns:
            bool: True if available, False otherwise
        """
        # Refresh model list if empty
        if not self.available_models:
            self.refresh_available_models()
            
        # Check if model exists (exact match or as prefix)
        for model in self.available_models:
            if model['name'] == model_name or model['name'].startswith(f"{model_name}:"):
                return True
        return False
    
    def find_embedding_model(self) -> str:
        """
        Find the best available embedding model.
        
        Returns:
            str: Name of the best available embedding model
        """
        # Preference order for embedding models
        embedding_models = ["nomic-embed-text", "granite-embedding:278m", "granite-embedding:30m", "all-MiniLM"]
        
        for model_name in embedding_models:
            if self.is_model_available(model_name):
                return model_name
                
        # If no specific embedding model is found, return the default
        return self.embedding_model
    
    def find_generation_model(self) -> str:
        """
        Find the best available generation model.
        
        Returns:
            str: Name of the best available generation model
        """
        # Check if default model is available
        if self.is_model_available(self.model):
            return self.model
            
        # Try popular fallback models
        fallback_models = ["llama3:8b", "llama3:8b-instruct", "llama3", "llama2", "mistral"]
        
        for model_name in fallback_models:
            if self.is_model_available(model_name):
                return model_name
                
        # If nothing specific is found, return the first available model
        if self.available_models:
            return self.available_models[0]['name']
            
        # Last resort - return the default even if not available
        return self.model
    
    def get_models_by_family(self, family: str) -> List[Dict[str, Any]]:
        """
        Get all models belonging to a specific family.
        
        Args:
            family: The model family to filter by
            
        Returns:
            List of models in the specified family
        """
        return [
            model for model in self.available_models 
            if model.get('details', {}).get('family') == family or 
               family in (model.get('details', {}).get('families') or [])
        ]
    
    def export_models_config(self, file_path: str = "models_config.yaml") -> None:
        """
        Export available models to a YAML configuration file.
        
        Args:
            file_path: Path to save the YAML file
        """
        # Refresh models list
        models = self.refresh_available_models()
        
        # Organize models by family
        models_by_family = {}
        for model in models:
            family = model.get('details', {}).get('family', 'other')
            if family not in models_by_family:
                models_by_family[family] = []
            models_by_family[family].append(model)
        
        # Create config structure
        config = {
            'default_generation_model': self.find_generation_model(),
            'default_embedding_model': self.find_embedding_model(),
            'models_by_family': models_by_family,
            'all_models': [model['name'] for model in models],
            'preferred_models': {
                'generation': ['llama3:8b-instruct-fp16', 'llama3:8b', 'deepseek-coder:6.7b'],
                'embedding': ['nomic-embed-text', 'granite-embedding:278m'],
                'coding': ['deepseek-coder:6.7b', 'llama3:8b-instruct-fp16']
            }
        }
        
        # Write to file
        with open(file_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
        return config
    
    def generate(self, prompt: str, model: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate text using the specified model.
        
        Args:
            prompt: The prompt to generate from
            model: Optional model override (uses default if not specified)
            options: Additional options for generation
            
        Returns:
            str: The generated text
        """
        # If model is specified but not available, try to find an alternative
        if model and not self.is_model_available(model):
            print(f"Warning: Model '{model}' not available. Falling back to default.")
            model = self.find_generation_model()
            
        model_to_use = model or self.model
        
        payload = {
            "model": model_to_use,
            "prompt": prompt,
            "temperature": options.get("temperature", self.temperature) if options else self.temperature,
            "stream": False
        }
        
        # Add any additional options
        if options:
            for key, value in options.items():
                if key not in payload:
                    payload[key] = value
        
        try:
            response = requests.post(self.generate_endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except Exception as e:
            print(f"Error generating text: {e}")
            return f"Error: {str(e)}"
    
    def get_embeddings(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Get embeddings for the given text.
        
        Args:
            text: The text to embed
            model: Optional model override for embeddings
            
        Returns:
            List[float]: The embedding vector
        """
        # If model is specified but not available, try to find an alternative
        if model and not self.is_model_available(model):
            print(f"Warning: Embedding model '{model}' not available. Falling back to default.")
            model = self.find_embedding_model()
            
        model_to_use = model or self.embedding_model
        
        payload = {
            "model": model_to_use,
            "prompt": text
        }
        
        try:
            response = requests.post(self.embedding_endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("embedding", [])
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return []
    
    def generate_with_json_output(self, prompt: str, model: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate text and attempt to parse it as JSON.
        
        Args:
            prompt: The prompt to generate from
            model: Optional model override
            options: Additional options for generation
            
        Returns:
            Dict: The parsed JSON or an error dict
        """
        # Add JSON formatting instructions to the prompt if not already present
        if "JSON" not in prompt and "json" not in prompt:
            prompt += "\n\nPlease format your response as a valid JSON object."
        
        response_text = self.generate(prompt, model, options)
        
        try:
            # Try to find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > 0:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"error": "No JSON found in response", "raw_response": response_text}
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON", "raw_response": response_text}


class LLMClientFactory:
    """Factory for creating LLM clients based on configuration."""
    
    @staticmethod
    def create_client(client_type: str = "ollama", config: Optional[Dict[str, Any]] = None) -> Any:
        """
        Create an LLM client of the specified type.
        
        Args:
            client_type: Type of client to create ("ollama" supported)
            config: Configuration dictionary
            
        Returns:
            LLM client instance
        """
        if client_type.lower() == "ollama":
            if config:
                return OllamaClient(
                    base_url=config.get("base_url", "http://localhost:11434"),
                    model=config.get("model", "llama3:8b-instruct-fp16"),
                    embedding_model=config.get("embedding_model", "nomic-embed-text"),
                    temperature=config.get("temperature", 0.7),
                    config_path=config.get("config_path"),
                    auto_detect_models=config.get("auto_detect_models", True)
                )
            else:
                return OllamaClient()
        else:
            raise ValueError(f"Unsupported client type: {client_type}")


# Configuration functions
def load_config(config_path: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict: Configuration dictionary
    """
    default_paths = [
        Path.cwd() / "config" / "llm_config.yaml",
        Path.cwd() / "llm_config.yaml",
        Path.home() / ".config" / "crewai" / "llm_config.yaml"
    ]
    
    if config_path:
        path = Path(config_path)
    else:
        # Try default paths
        for path in default_paths:
            if path.exists():
                break
        else:
            # No config found, return empty dict
            return {}
    
    try:
        if path.exists():
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}


# Helper function to get a client with default configuration
def get_default_client() -> OllamaClient:
    """
    Get a default Ollama client.
    
    Returns:
        OllamaClient: A configured client
    """
    config = load_config()
    return LLMClientFactory.create_client("ollama", config)


# Example usage for generating a models config file
def generate_models_config(output_path: str = "models_config.yaml") -> None:
    """
    Generate a YAML configuration file with all available models.
    
    Args:
        output_path: Path to save the YAML file
    """
    client = OllamaClient()
    config = client.export_models_config(output_path)
    print(f"Generated models configuration at {output_path}")
    return config


if __name__ == "__main__":
    # Example of generating a models config file
    generate_models_config()
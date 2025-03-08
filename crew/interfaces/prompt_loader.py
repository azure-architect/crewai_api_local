# crew/clients/prompt_loader.py
import os
import yaml
import logging
from typing import Optional, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_prompt(tool_type: str, prompt_variant: str = "standard") -> Optional[str]:
    """
    Load a specific prompt template.
    
    Args:
        tool_type: The type of tool (keyword_extraction, theme_extraction, etc.)
        prompt_variant: The variant of the prompt (standard, technical, etc.)
        
    Returns:
        str or None: The prompt template text, or None if not found
    """
    # Get the base directory of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", tool_type, f"{prompt_variant}.yml")
    
    try:
        with open(prompt_path, 'r') as f:
            prompt_data = yaml.safe_load(f)
            return prompt_data.get('template_text', '')
    except Exception as e:
        logger.error(f"Error loading prompt from {prompt_path}: {e}")
        return None

def get_prompt_metadata(tool_type: str, prompt_variant: str = "standard") -> Optional[Dict[str, Any]]:
    """
    Load a specific prompt template with its metadata.
    
    Args:
        tool_type: The type of tool (keyword_extraction, theme_extraction, etc.)
        prompt_variant: The variant of the prompt (standard, technical, etc.)
        
    Returns:
        Dict or None: The full prompt data including metadata, or None if not found
    """
    # Get the base directory of the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompts", tool_type, f"{prompt_variant}.yml")
    
    try:
        with open(prompt_path, 'r') as f:
            prompt_data = yaml.safe_load(f)
            return prompt_data
    except Exception as e:
        logger.error(f"Error loading prompt from {prompt_path}: {e}")
        return None

def get_available_prompt_variants(tool_type: str) -> list:
    """
    Get available prompt variants for a tool type.
    
    Args:
        tool_type: The type of tool
        
    Returns:
        list: Available prompt variants
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_dir = os.path.join(base_dir, "prompts", tool_type)
    
    variants = []
    
    try:
        if os.path.exists(prompt_dir):
            for filename in os.listdir(prompt_dir):
                if filename.endswith('.yml'):
                    variants.append(filename[:-4])  # Remove .yml extension
    except Exception as e:
        logger.error(f"Error getting prompt variants for {tool_type}: {e}")
    
    return variants

def list_tool_types() -> list:
    """
    List all available tool types based on prompt directories.
    
    Returns:
        list: Available tool types
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_dir = os.path.join(base_dir, "prompts")
    
    tool_types = []
    
    try:
        if os.path.exists(prompts_dir):
            tool_types = [d for d in os.listdir(prompts_dir) 
                         if os.path.isdir(os.path.join(prompts_dir, d))]
    except Exception as e:
        logger.error(f"Error listing tool types: {e}")
    
    return tool_types
#!/usr/bin/env python3
# create_llm_tools.py

import os
import sys
from pathlib import Path

# Template for the tool files
TOOL_TEMPLATE = '''from crew.tools.base_tool import BaseTool
from crew.interfaces.prompt_loader import get_prompt
import json

def create_{tool_type}_tool(llm_client):
    """
    Creates a tool for {tool_description}.
    
    Args:
        llm_client: The LLM client to use for {tool_operation}
        
    Returns:
        Tool: A CrewAI tool for {tool_type_readable}
    """
    def {function_name}(content: str, variant: str = "{default_variant}"):
        """
        {function_description}
        
        Args:
            content: The {content_description} to analyze
            variant: The prompt variant to use (default: {default_variant})
            
        Returns:
            Dict: Dictionary containing {return_description}
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt("{prompt_category}", variant)
        
        if not prompt_template:
            return {{
                "error": f"Prompt template not found for {prompt_category}/{{variant}}"
            }}
        
        # Format the prompt with the content
        formatted_prompt = prompt_template.format(content=content)
        
        # Make the LLM call
        response = llm_client.generate(formatted_prompt)
        
        # Parse the response to extract JSON
        try:
            # Find JSON in the response
            json_start = response.find('{{')
            json_end = response.rfind('}}') + 1
            if json_start >= 0 and json_end > 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback if proper JSON not found
                return {{
                    {fallback_fields}
                    "error": "Could not extract structured data from LLM response"
                }}
        except Exception as e:
            print(f"Error parsing LLM response: {{e}}")
            return {{
                {fallback_fields}
                "error": f"Error processing response: {{str(e)}}"
            }}
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="{function_name}",
        func={function_name},
        description="{tool_description}",
        parameters={{
            "type": "object",
            "properties": {{
                "content": {{
                    "type": "string",
                    "description": "The {content_description} to analyze for {tool_type_readable}"
                }},
                "variant": {{
                    "type": "string",
                    "description": "The prompt variant to use (default: {default_variant})",
                    "default": "{default_variant}"{variant_enum}
                }}
            }},
            "required": ["content"]
        }}
    )
'''

# Tool configurations
TOOLS = [
    {
        "tool_type": "code_analysis",
        "tool_type_readable": "code analysis",
        "tool_description": "analyzing code structure, quality, and functionality",
        "tool_operation": "analysis",
        "function_name": "analyze_code",
        "function_description": "Analyze code from the given content.",
        "content_description": "code content",
        "return_description": "code analysis results",
        "default_variant": "standard",
        "prompt_category": "code_analysis",
        "fallback_fields": '"language": "",\n                    "purpose": "",\n                    ',
        "variant_enum": ""
    },
    {
        "tool_type": "content_repurposing",
        "tool_type_readable": "content repurposing",
        "tool_description": "identifying content repurposing opportunities",
        "tool_operation": "analysis",
        "function_name": "identify_repurposing_opportunities",
        "function_description": "Identify opportunities for repurposing content into different formats.",
        "content_description": "text content",
        "return_description": "repurposing opportunities",
        "default_variant": "standard",
        "prompt_category": "content_repurposing",
        "fallback_fields": '"content_type": "",\n                    "repurposing_opportunities": [],\n                    ',
        "variant_enum": ""
    },
    {
        "tool_type": "entity_extraction",
        "tool_type_readable": "entity extraction",
        "tool_description": "extracting named entities and their relationships from content",
        "tool_operation": "extraction",
        "function_name": "extract_entities",
        "function_description": "Extract named entities from the given content.",
        "content_description": "text content",
        "return_description": "extracted entities and relationships",
        "default_variant": "standard",
        "prompt_category": "entity_extraction",
        "fallback_fields": '"people": [],\n                    "organizations": [],\n                    "locations": [],\n                    ',
        "variant_enum": ""
    },
    {
        "tool_type": "section_analyzer",
        "tool_type_readable": "section analysis",
        "tool_description": "analyzing document structure, sections, and organization",
        "tool_operation": "analysis",
        "function_name": "analyze_sections",
        "function_description": "Analyze document structure and sections from the given content.",
        "content_description": "document content",
        "return_description": "section analysis results",
        "default_variant": "standard",
        "prompt_category": "section_analyzer",
        "fallback_fields": '"document_type": "",\n                    "sections": [],\n                    ',
        "variant_enum": ""
    },
    {
        "tool_type": "summary_generation",
        "tool_type_readable": "summary generation",
        "tool_description": "generating summaries of content",
        "tool_operation": "generation",
        "function_name": "generate_summary",
        "function_description": "Generate a summary of the given content.",
        "content_description": "text content",
        "return_description": "the generated summary",
        "default_variant": "executive",
        "prompt_category": "summary_generation",
        "fallback_fields": 'summary_key = f"{variant}_summary",\n                    summary_key: "",\n                    "key_points": [],\n                    ',
        "variant_enum": ',\n                    "enum": ["executive", "technical"]'
    }
]

def create_tool_file(tool_config, output_dir):
    """Create a tool file based on the template and configuration."""
    # Format the template with the tool configuration
    file_content = TOOL_TEMPLATE.format(**tool_config)
    
    # Create the output file path
    filename = f"LLM_{tool_config['tool_type']}_tool.py"
    file_path = os.path.join(output_dir, filename)
    
    # Write the file
    with open(file_path, 'w') as f:
        f.write(file_content)
    
    print(f"Created tool file: {file_path}")

def main():
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if 'crew' in script_dir:
        # If script is already in the crew directory
        project_root = os.path.dirname(os.path.dirname(script_dir))
    else:
        # Assume script is in project root
        project_root = script_dir
    
    # Create the output directory if it doesn't exist
    output_dir = os.path.join(project_root, 'crew', 'tools')
    os.makedirs(output_dir, exist_ok=True)
    
    # Create each tool file
    for tool_config in TOOLS:
        create_tool_file(tool_config, output_dir)
    
    print(f"All {len(TOOLS)} tool files have been created successfully.")

if __name__ == "__main__":
    main()
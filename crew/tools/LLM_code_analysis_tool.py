from crew.tools.base_tool import BaseTool
from crew.interfaces.prompt_loader import get_prompt
import json

def create_code_analysis_tool(llm_client):
    """
    Creates a tool for analyzing code structure, quality, and functionality.
    
    Args:
        llm_client: The LLM client to use for analysis
        
    Returns:
        Tool: A CrewAI tool for code analysis
    """
    def analyze_code(content: str, variant: str = "standard"):
        """
        Analyze code from the given content.
        
        Args:
            content: The code content to analyze
            variant: The prompt variant to use (default: standard)
            
        Returns:
            Dict: Dictionary containing code analysis results
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt("code_analysis", variant)
        
        if not prompt_template:
            return {
                "error": f"Prompt template not found for code_analysis/{variant}"
            }
        
        # Format the prompt with the content
        formatted_prompt = prompt_template.format(content=content)
        
        # Make the LLM call
        response = llm_client.generate(formatted_prompt)
        
        # Parse the response to extract JSON
        try:
            # Find JSON in the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback if proper JSON not found
                return {
                    "language": "",
                    "purpose": "",
                    
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "language": "",
                    "purpose": "",
                    
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="analyze_code",
        func=analyze_code,
        description="analyzing code structure, quality, and functionality",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The code content to analyze for code analysis"
                },
                "variant": {
                    "type": "string",
                    "description": "The prompt variant to use (default: standard)",
                    "default": "standard"
                }
            },
            "required": ["content"]
        }
    )

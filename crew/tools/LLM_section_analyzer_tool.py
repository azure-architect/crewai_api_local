from crew.tools.base_tool import BaseTool
from crew.interfaces.prompt_loader import get_prompt
import json

def create_section_analyzer_tool(llm_client):
    """
    Creates a tool for analyzing document structure, sections, and organization.
    
    Args:
        llm_client: The LLM client to use for analysis
        
    Returns:
        Tool: A CrewAI tool for section analysis
    """
    def analyze_sections(content: str, variant: str = "standard"):
        """
        Analyze document structure and sections from the given content.
        
        Args:
            content: The document content to analyze
            variant: The prompt variant to use (default: standard)
            
        Returns:
            Dict: Dictionary containing section analysis results
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt("section_analyzer", variant)
        
        if not prompt_template:
            return {
                "error": f"Prompt template not found for section_analyzer/{variant}"
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
                    "document_type": "",
                    "sections": [],
                    
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "document_type": "",
                    "sections": [],
                    
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="analyze_sections",
        func=analyze_sections,
        description="analyzing document structure, sections, and organization",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The document content to analyze for section analysis"
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

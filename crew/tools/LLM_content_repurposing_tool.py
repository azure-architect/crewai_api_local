from crew.tools.base_tool import BaseTool
from crew.interfaces.prompt_loader import get_prompt
import json

def create_content_repurposing_tool(llm_client):
    """
    Creates a tool for identifying content repurposing opportunities.
    
    Args:
        llm_client: The LLM client to use for analysis
        
    Returns:
        Tool: A CrewAI tool for content repurposing
    """
    def identify_repurposing_opportunities(content: str, variant: str = "standard"):
        """
        Identify opportunities for repurposing content into different formats.
        
        Args:
            content: The text content to analyze
            variant: The prompt variant to use (default: standard)
            
        Returns:
            Dict: Dictionary containing repurposing opportunities
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt("content_repurposing", variant)
        
        if not prompt_template:
            return {
                "error": f"Prompt template not found for content_repurposing/{variant}"
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
                    "content_type": "",
                    "repurposing_opportunities": [],
                    
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "content_type": "",
                    "repurposing_opportunities": [],
                    
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="identify_repurposing_opportunities",
        func=identify_repurposing_opportunities,
        description="identifying content repurposing opportunities",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to analyze for content repurposing"
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

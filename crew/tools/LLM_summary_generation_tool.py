from crew.tools.base_tool import BaseTool
from crew.interfaces.prompt_loader import get_prompt
import json

def create_summary_generation_tool(llm_client):
    """
    Creates a tool for generating summaries of content.
    
    Args:
        llm_client: The LLM client to use for generation
        
    Returns:
        Tool: A CrewAI tool for summary generation
    """
    def generate_summary(content: str, variant: str = "executive"):
        """
        Generate a summary of the given content.
        
        Args:
            content: The text content to analyze
            variant: The prompt variant to use (default: executive)
            
        Returns:
            Dict: Dictionary containing the generated summary
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt("summary_generation", variant)
        
        if not prompt_template:
            return {
                "error": f"Prompt template not found for summary_generation/{variant}"
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
                    summary_key = f"{variant}_summary"
                    summary_key: "",
                    "key_points": [],
                    
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                summary_key = f"{variant}_summary",
                    summary_key: "",
                    "key_points": [],
                    
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="generate_summary",
        func=generate_summary,
        description="generating summaries of content",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to analyze for summary generation"
                },
                "variant": {
                    "type": "string",
                    "description": "The prompt variant to use (default: executive)",
                    "default": "executive",
                    "enum": ["executive", "technical"]
                }
            },
            "required": ["content"]
        }
    )

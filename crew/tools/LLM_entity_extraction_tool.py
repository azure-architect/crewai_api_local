from crew.tools.base_tool import BaseTool
from crew.interfaces.prompt_loader import get_prompt
import json

def create_entity_extraction_tool(llm_client):
    """
    Creates a tool for extracting named entities and their relationships from content.
    
    Args:
        llm_client: The LLM client to use for extraction
        
    Returns:
        Tool: A CrewAI tool for entity extraction
    """
    def extract_entities(content: str, variant: str = "standard"):
        """
        Extract named entities from the given content.
        
        Args:
            content: The text content to analyze
            variant: The prompt variant to use (default: standard)
            
        Returns:
            Dict: Dictionary containing extracted entities and relationships
        """
        # Get the appropriate prompt template
        prompt_template = get_prompt("entity_extraction", variant)
        
        if not prompt_template:
            return {
                "error": f"Prompt template not found for entity_extraction/{variant}"
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
                    "people": [],
                    "organizations": [],
                    "locations": [],
                    
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "people": [],
                    "organizations": [],
                    "locations": [],
                    
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="extract_entities",
        func=extract_entities,
        description="extracting named entities and their relationships from content",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to analyze for entity extraction"
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

from crew.tools.base_tool import BaseTool
import json

def create_theme_extraction_tool(llm_client):
    """
    Creates a tool for extracting themes from text content.
    
    Args:
        llm_client: The LLM client to use for extraction
        
    Returns:
        Tool: A CrewAI tool for theme extraction
    """
    def extract_themes(content: str):
        """
        Extract themes from the given content.
        
        Args:
            content: The text content to analyze
            
        Returns:
            Dict: Dictionary containing extracted themes and metadata
        """
        # Extensive prompt for theme extraction
        prompt = """
        Analyze the following content and identify the main themes and topics.
        Consider:
        - Overall subject matter
        - Recurring ideas
        - Implied perspectives or worldviews
        - Business domains represented
        - Philosophical or theoretical frameworks
        
        Return ONLY a JSON object with the following structure:
        {
            "primary_theme": "The main overarching theme",
            "secondary_themes": ["theme1", "theme2", "theme3"],
            "business_domains": ["domain1", "domain2"],
            "philosophical_frameworks": ["framework1", "framework2"],
            "summary": "A brief 1-2 sentence summary of the content's thematic elements"
        }
        
        Content to analyze:
        {content}
        """
        
        # Make the LLM call
        formatted_prompt = prompt.format(content=content)
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
                    "primary_theme": "",
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "primary_theme": "",
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="extract_themes",
        func=extract_themes,
        description="Extracts themes, domains, and frameworks from content",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to analyze for theme extraction"
                }
            },
            "required": ["content"]
        }
    )
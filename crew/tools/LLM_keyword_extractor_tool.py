from crew.tools.base_tool import BaseTool
import json

def create_keyword_extraction_tool(llm_client):
    """
    Creates a tool for extracting keywords from text content.
    
    Args:
        llm_client: The LLM client to use for extraction
        
    Returns:
        Tool: A CrewAI tool for keyword extraction
    """
    def extract_keywords(content: str):
        """
        Extract keywords from the given content.
        
        Args:
            content: The text content to analyze
            
        Returns:
            Dict: Dictionary containing extracted keywords and metadata
        """
        # Extensive prompt for keyword extraction
        prompt = """
        Analyze the following content and extract the most relevant keywords.
        Focus on:
        - Industry-specific terminology
        - Technical concepts
        - Marketable terms
        - Domain-specific vocabulary
        - Trending topics mentioned
        
        Return ONLY a JSON object with the following structure:
        {
            "primary_keywords": ["keyword1", "keyword2", "keyword3"],
            "secondary_keywords": ["keyword4", "keyword5", "keyword6"],
            "technical_terms": ["term1", "term2", "term3"],
            "marketable_concepts": ["concept1", "concept2", "concept3"]
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
                    "primary_keywords": [],
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "primary_keywords": [],
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="extract_keywords",
        func=extract_keywords,
        description="Extracts keywords, technical terms, and marketable concepts from content",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to analyze for keyword extraction"
                }
            },
            "required": ["content"]
        }
    )
from crew.tools.base_tool import BaseTool
import json

def create_process_extraction_tool(llm_client):
    """
    Creates a tool for extracting processes and steps from content.
    
    Args:
        llm_client: The LLM client to use for extraction
        
    Returns:
        Tool: A CrewAI tool for process extraction
    """
    def extract_processes(content: str):
        """
        Extract processes, workflows, and steps from the given content.
        
        Args:
            content: The text content to analyze
            
        Returns:
            Dict: Dictionary containing extracted processes and workflows
        """
        # Extensive prompt for process extraction
        prompt = """
        Analyze the following content and identify any processes, workflows, or step-by-step instructions.
        Focus on:
        - Sequential steps or procedures
        - Workflows or business processes
        - Methodologies described
        - Decision trees or branching logic
        - Requirements or prerequisites
        
        Return ONLY a JSON object with the following structure:
        {
            "identified_processes": [
                {
                    "name": "Name of process 1",
                    "steps": ["step 1", "step 2", "step 3"],
                    "is_complete": true/false,
                    "prerequisites": ["prerequisite 1", "prerequisite 2"],
                    "estimated_complexity": "low/medium/high"
                }
            ],
            "workflows": [
                {
                    "name": "Name of workflow 1",
                    "description": "Brief description",
                    "steps": ["step 1", "step 2", "step 3"]
                }
            ],
            "decision_points": [
                {
                    "decision": "Decision to make",
                    "options": ["option 1", "option 2"],
                    "considerations": ["consideration 1", "consideration 2"]
                }
            ]
        }
        
        If no clear processes are identified, return an empty array for each category.
        
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
                    "identified_processes": [],
                    "workflows": [],
                    "decision_points": [],
                    "error": "Could not extract structured data from LLM response"
                }
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {
                "identified_processes": [],
                "workflows": [],
                "decision_points": [],
                "error": f"Error processing response: {str(e)}"
            }
    
    # Create and return the tool using BaseTool factory
    return BaseTool.create_tool(
        name="extract_processes",
        func=extract_processes,
        description="Extracts processes, workflows, and step-by-step instructions from content",
        parameters={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The text content to analyze for process extraction"
                }
            },
            "required": ["content"]
        }
    )
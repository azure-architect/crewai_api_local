from typing import Callable, Optional, Dict, Any
from crewai.tools import Tool

class BaseTool:
    """Base class for creating tools in the CrewAI-Local system."""
    
    @staticmethod
    def create_tool(
        name: str,
        func: Callable,
        description: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Tool:
        """
        Create a CrewAI tool with the specified parameters.
        
        Args:
            name: The name of the tool
            func: The function to execute
            description: The description of the tool
            parameters: The parameters for the tool
            
        Returns:
            Tool: A CrewAI tool
        """
        return Tool(
            name=name,
            func=func,
            description=description,
            parameters=parameters or {}
        )

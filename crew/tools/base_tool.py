from typing import Callable, Optional, Dict, Any

# Check which version of the CrewAI tools API is available
try:
    # Try importing Tool directly
    from crewai.tools import Tool
except ImportError:
    try:
        # Try importing BaseTool and use that instead
        from crewai import BaseTool as Tool
    except ImportError:
        # If neither works, create a compatible Tool class
        class Tool:
            """Compatibility class for CrewAI Tool."""
            
            def __init__(self, name, func, description, parameters=None):
                self.name = name
                self.func = func
                self.description = description
                self.parameters = parameters or {}


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
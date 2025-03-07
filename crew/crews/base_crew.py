from crewai import Crew, Agent, Task
from typing import List, Optional, Dict, Any

class BaseCrew:
    """Base class for creating crews in the CrewAI-Local system."""
    
    @staticmethod
    def create_crew(
        agents: List[Agent],
        tasks: List[Task],
        verbose: bool = False,
        process: Optional[str] = "sequential",
        config: Optional[Dict[str, Any]] = None
    ) -> Crew:
        """
        Create a CrewAI crew with the specified agents and tasks.
        
        Args:
            agents: List of agents in the crew
            tasks: List of tasks for the crew to perform
            verbose: Whether to enable verbose output
            process: The process to use for task execution
            config: Additional configuration for the crew
            
        Returns:
            Crew: A CrewAI crew
        """
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=verbose,
            process=process,
            config=config or {}
        )

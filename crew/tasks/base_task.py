from crewai import Task, Agent
from typing import List, Optional, Union, Callable

class BaseTask:
    """Base class for creating tasks in the CrewAI-Local system."""
    
    @staticmethod
    def create_task(
        description: str,
        agent: Agent,
        expected_output: Optional[str] = None,
        tools: Optional[List] = None,
        async_execution: bool = False,
        callback: Optional[Callable] = None
    ) -> Task:
        """
        Create a CrewAI task with the specified parameters.
        
        Args:
            description: The description of the task
            agent: The agent assigned to the task
            expected_output: The expected output format
            tools: List of tools available for the task
            async_execution: Whether to execute the task asynchronously
            callback: A callback function to execute after the task
            
        Returns:
            Task: A CrewAI task
        """
        return Task(
            description=description,
            agent=agent,
            expected_output=expected_output,
            tools=tools or [],
            async_execution=async_execution,
            callback=callback
        )

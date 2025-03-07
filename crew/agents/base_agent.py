from crewai import Agent
from typing import List, Optional

class BaseAgent:
    """Base class for creating agents in the CrewAI-Local system."""
    
    @staticmethod
    def create_agent(
        name: str,
        role: str,
        goal: str,
        backstory: Optional[str] = None,
        verbose: bool = False,
        allow_delegation: bool = True,
        tools: List = None
    ) -> Agent:
        """
        Create a CrewAI agent with the specified parameters.
        
        Args:
            name: The name of the agent
            role: The role of the agent
            goal: The goal the agent is trying to achieve
            backstory: The backstory of the agent
            verbose: Whether to enable verbose output
            allow_delegation: Whether to allow delegation to other agents
            tools: List of tools the agent can use
            
        Returns:
            Agent: A CrewAI agent
        """
        return Agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory or f"{name} is an expert in their field.",
            verbose=verbose,
            allow_delegation=allow_delegation,
            tools=tools or []
        )

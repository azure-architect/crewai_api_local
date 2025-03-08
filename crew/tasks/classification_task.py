from crew.tasks.base_task import BaseTask
from crewai import Task, Agent

def create_classification_task(agent, expected_output=None):
    """
    Create a task for content classification.
    
    Args:
        agent: The classification agent
        expected_output: The expected output format
        
    Returns:
        Task: A CrewAI task for content classification
    """
    description = (
        "Analyze the content of provided files to:"
        "\n1. Detect all hashtags in the content"
        "\n2. Extract frontmatter metadata"
        "\n3. Classify the content based on hashtags and file characteristics"
        "\n4. Determine appropriate storage decisions based on source-based partitioning"
        "\n\nProvide a classification result with file information, content type, hashtags, "
        "metadata, and storage decisions."
    )
    
    return BaseTask.create_task(
        description=description,
        agent=agent,
        expected_output=expected_output or "Dictionary containing classification information for each file processed.",
        async_execution=False
    )
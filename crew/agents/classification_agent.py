from crew.agents.base_agent import BaseAgent
from crewai import Agent
from typing import List, Optional, Dict, Any
import re
from pathlib import Path


class ClassificationAgent:
    """Agent factory for content classification functionality."""
    
    @staticmethod
    def create_agent(
        name: str = "Content Classifier",
        role: str = "Content Analyzer",
        goal: str = "Analyze content to detect hashtags and classify for appropriate storage",
        backstory: Optional[str] = None,
        verbose: bool = False,
        allow_delegation: bool = True,
        tools: List = None
    ) -> Agent:
        """
        Create a Classification Agent using the BaseAgent factory.
        
        Args:
            name: The name of the agent
            role: The role of the agent
            goal: The goal the agent is trying to achieve
            backstory: The backstory of the agent
            verbose: Whether to enable verbose output
            allow_delegation: Whether to allow delegation to other agents
            tools: List of tools the agent can use
            
        Returns:
            Agent: A CrewAI agent configured for content classification
        """
        # Create default backstory if none provided
        if not backstory:
            backstory = (
                f"{name} specializes in analyzing content to identify hashtags, "
                f"extract metadata, and determine how the content should be "
                f"partitioned across storage systems. It ensures content is properly "
                f"categorized based on source markers like hashtags."
            )
        
        # Create agent using the BaseAgent factory
        agent = BaseAgent.create_agent(
            name=name,
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=verbose,
            allow_delegation=allow_delegation,
            tools=tools or []
        )
        
        # Add classification methods to the agent
        agent.detect_hashtags = ClassificationAgent._detect_hashtags.__get__(agent)
        agent.extract_frontmatter = ClassificationAgent._extract_frontmatter.__get__(agent)
        agent.classify_content = ClassificationAgent._classify_content.__get__(agent)
        
        return agent
    
    @staticmethod
    def _detect_hashtags(self, file_path):
        """
        Detect hashtags in a file to determine classification.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            list: Detected hashtags in the file
        """
        hashtags = []
        try:
            # Convert to Path object if it's a string
            if isinstance(file_path, str):
                file_path = Path(file_path)
                
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Find all hashtags using regex
                hashtags = re.findall(r'#(\w+)', content)
                
                # Deduplicate and normalize
                hashtags = list(set([tag.lower() for tag in hashtags]))
                
                print(f"Detected hashtags in {file_path.name}: {hashtags}")
                return hashtags
        except Exception as e:
            print(f"Error detecting hashtags in {file_path}: {e}")
            return []
    
    @staticmethod
    def _extract_frontmatter(self, file_path):
        """
        Extract metadata from the file's frontmatter.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            dict: Metadata extracted from the file
        """
        metadata = {}
        try:
            # Convert to Path object if it's a string
            if isinstance(file_path, str):
                file_path = Path(file_path)
                
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Check for frontmatter between --- markers
                frontmatter_match = re.search(r'^---\s+(.*?)\s+---', content, re.DOTALL)
                if frontmatter_match:
                    frontmatter_content = frontmatter_match.group(1)
                    
                    # Parse key-value pairs
                    for line in frontmatter_content.split('\n'):
                        if ':' in line:
                            key, value = line.split(':', 1)
                            metadata[key.strip()] = value.strip()
            
            print(f"Extracted frontmatter from {file_path.name}: {metadata}")
            return metadata
        except Exception as e:
            print(f"Error extracting frontmatter from {file_path}: {e}")
            return metadata
    
    @staticmethod
    def _classify_content(self, file_path):
        """
        Classify content based on hashtags and metadata.
        
        Args:
            file_path: Path to the file to classify
            
        Returns:
            dict: Classification information including hashtags, metadata, and storage decisions
        """
        try:
            # Convert to Path object if it's a string
            if isinstance(file_path, str):
                file_path = Path(file_path)
                
            # Detect hashtags and extract metadata
            hashtags = self.detect_hashtags(file_path)
            metadata = self.extract_frontmatter(file_path)
            
            # Determine content type based on hashtags or file extension
            content_type = "unknown"
            if any(tag in hashtags for tag in ["youtube", "video"]):
                content_type = "video"
            elif any(tag in hashtags for tag in ["article", "blog"]):
                content_type = "article"
            elif any(tag in hashtags for tag in ["book"]):
                content_type = "book"
            elif any(tag in hashtags for tag in ["process", "workflow"]):
                content_type = "process"
            else:
                # Fallback to file extension
                if file_path.suffix.lower() in [".md", ".txt"]:
                    content_type = "note"
                elif file_path.suffix.lower() in [".pdf"]:
                    content_type = "document"
            
            # Build classification result
            classification = {
                "file_path": str(file_path),
                "filename": file_path.name,
                "content_type": content_type,
                "hashtags": hashtags,
                "metadata": metadata,
                # Storage decisions based on source partitioning via hashtags
                "storage": {
                    "obsidian": True,  # Always store in Obsidian
                    "vector_db": len(hashtags) > 0,  # Store in vector DB if hashtags exist
                    "sql_db": content_type in ["process", "workflow"]  # Store process info in SQL
                }
            }
            
            print(f"Classified {file_path.name} as {content_type} with storage decisions: {classification['storage']}")
            return classification
        except Exception as e:
            print(f"Error classifying content in {file_path}: {e}")
            return {
                "file_path": str(file_path),
                "filename": file_path.name if hasattr(file_path, "name") else "unknown",
                "content_type": "unknown",
                "hashtags": [],
                "metadata": {},
                "storage": {"obsidian": True, "vector_db": False, "sql_db": False}
            }
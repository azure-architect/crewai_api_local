from crew.agents.base_agent import BaseAgent
from crewai import Agent
from typing import List, Optional
import os
import time
from pathlib import Path
from config.settings import settings  # Import your settings module


class FileWatchingAgent:
    """Agent for monitoring directories and detecting new files."""
    
    @staticmethod
    def create_agent(
        name: str = "File Watcher",
        role: str = "File System Monitor",
        goal: str = "Monitor directories for new files and detect content for processing",
        backstory: Optional[str] = None,
        watch_directory: Optional[str] = None,
        poll_interval: int = 5,
        verbose: bool = False,
        allow_delegation: bool = True,
        tools: List = None
    ) -> Agent:
        """
        Create a File Watching Agent using the BaseAgent factory.
        
        Args:
            name: The name of the agent
            role: The role of the agent
            goal: The goal the agent is trying to achieve
            backstory: The backstory of the agent
            watch_directory: Directory to monitor for new files (overrides env setting)
            poll_interval: Interval in seconds between file system checks
            verbose: Whether to enable verbose output
            allow_delegation: Whether to allow delegation to other agents
            tools: List of tools the agent can use
            
        Returns:
            Agent: A CrewAI agent configured for file watching
        """
        # Get watch directory from settings or use provided value
        watch_directory = watch_directory or getattr(settings, "watcher_path", None)
        
        # Fall back to default if still not set
        if not watch_directory:
            watch_directory = os.path.expanduser("~/Documents/Inbox")
            print(f"No watch directory specified in settings, using default: {watch_directory}")
        
        # Use Path to handle spaces in path properly
        watch_directory = Path(watch_directory)
        
        # Create default backstory if none provided
        if not backstory:
            backstory = (
                f"{name} specializes in monitoring file systems and detecting new content. "
                f"It watches specified directories and notifies when files are added or modified, "
                f"enabling prompt processing of new information."
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
        
        # Add file watching specific attributes
        agent.watch_directory = watch_directory
        agent.poll_interval = poll_interval
        agent.processed_files = set()
        agent.should_stop = False
        
        # Add file watching methods to the agent
        agent.start_watching = FileWatchingAgent._start_watching.__get__(agent)
        agent.stop_watching = FileWatchingAgent._stop_watching.__get__(agent)
        agent.process_new_file = FileWatchingAgent._process_new_file.__get__(agent)
        
        return agent
    
    @staticmethod
    def _start_watching(self):
        """Start watching for new files in the directory."""
        if not self.watch_directory.exists():
            self.watch_directory.mkdir(parents=True, exist_ok=True)
            print(f"Created watch directory: {self.watch_directory}")
            
        print(f"Started watching directory: {self.watch_directory}")
        self.should_stop = False
        
        try:
            while not self.should_stop:
                # Get all files in the directory
                current_files = set(self.watch_directory.glob('*.*'))
                
                # Find new files
                new_files = current_files - self.processed_files
                
                for file_path in new_files:
                    print(f"New file detected: {file_path}")
                    self.process_new_file(file_path)
                    
                    # Add to processed files
                    self.processed_files.add(file_path)
                
                # Sleep for the poll interval
                time.sleep(self.poll_interval)
                
        except Exception as e:
            print(f"Error watching files: {e}")
        
        print(f"Stopped watching directory: {self.watch_directory}")
    
    @staticmethod
    def _stop_watching(self):
        """Stop watching for new files."""
        self.should_stop = True
        print(f"Stopping file watcher...")
    
    @staticmethod
    def _process_new_file(self, file_path):
        """
        Process a newly detected file.
        
        Args:
            file_path: Path to the newly detected file
            
        Returns:
            dict: File information
        """
        try:
            # Extract basic file information
            file_info = {
                "path": str(file_path),
                "filename": file_path.name,
                "extension": file_path.suffix.lower(),
                "size": file_path.stat().st_size,
                "modified_time": file_path.stat().st_mtime,
                "created_time": file_path.stat().st_ctime
            }
            
            print(f"Processing new file: {file_info['filename']}")
            
            # In a real implementation, would delegate to other agents or notify the crew
            # Return the file information for use by other agents
            return file_info
            
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return None
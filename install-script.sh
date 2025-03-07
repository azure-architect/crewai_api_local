#!/bin/bash

# Create script to set up CrewAI-Local project structure
# Usage: ./setup_crewai_project.sh
# This script sets up the project in the current directory

set -e  # Exit on error

echo "Creating CrewAI-Local project structure in current directory"

# Create root level files
touch .env
touch main.py
touch pyproject.toml
touch README.md

# Create .gitignore with common Python ignores
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environments
venv/
ENV/
.env

# Poetry
.venv/
poetry.lock

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db
EOF

# Create API module
mkdir -p api/routers api/models api/dependencies
touch api/__init__.py
touch api/main.py
touch api/routers/__init__.py
touch api/routers/crews.py
touch api/routers/agents.py
touch api/routers/tasks.py
touch api/routers/tools.py
touch api/models/__init__.py
touch api/models/crews.py
touch api/models/agents.py
touch api/models/tasks.py
touch api/models/tools.py
touch api/dependencies/__init__.py
touch api/dependencies/db.py

# Create Crew module
mkdir -p crew/agents crew/crews crew/tasks crew/tools crew/utils
touch crew/__init__.py
touch crew/agents/__init__.py
touch crew/agents/base_agent.py
touch crew/crews/__init__.py
touch crew/crews/base_crew.py
touch crew/tasks/__init__.py
touch crew/tasks/base_task.py
touch crew/tools/__init__.py
touch crew/tools/base_tool.py
touch crew/utils/__init__.py
touch crew/utils/helpers.py

# Create config module
mkdir -p config
touch config/__init__.py
touch config/settings.py

# Create tests
mkdir -p tests/api tests/crew
touch tests/__init__.py
touch tests/conftest.py
touch tests/api/__init__.py
touch tests/api/test_routes.py
touch tests/crew/__init__.py
touch tests/crew/test_agents.py
touch tests/crew/test_crews.py
touch tests/crew/test_tasks.py
touch tests/crew/test_tools.py

# Add content to main.py
cat > main.py << 'EOF'
import uvicorn
from api.main import app

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
EOF

# Add content to pyproject.toml
cat > pyproject.toml << 'EOF'
[tool.poetry]
name = "crewai-local"
version = "0.1.0"
description = "CrewAI-Local with Supabase integration"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.109.0"
uvicorn = "^0.27.0"
supabase = "^2.3.0"
python-dotenv = "^1.0.0"
pydantic = "^2.6.0"
pydantic-settings = "^2.1.0"
crewai = "^0.28.0"  # Make sure to use the latest version

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.7.0"
ipython = "^8.14.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
EOF

# Add basic content to config/settings.py
cat > config/settings.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API settings
    api_title: str = "CrewAI-Local API"
    api_description: str = "API for CrewAI-Local with Supabase integration"
    api_version: str = "0.1.0"
    
    # Supabase settings
    supabase_url: str
    supabase_key: str
    
    # Application settings
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
EOF

# Add basic content to api/main.py
cat > api/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import settings
from api.routers import crews, agents, tasks, tools

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(crews.router)
app.include_router(agents.router)
app.include_router(tasks.router)
app.include_router(tools.router)


@app.get("/")
async def root():
    return {"message": "Welcome to CrewAI-Local API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
EOF

# Add basic content to api/dependencies/db.py
cat > api/dependencies/db.py << 'EOF'
from supabase import create_client
from config.settings import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)


def get_db():
    return supabase
EOF

# Create router files individually to avoid sed issues
# Crews router
cat > api/routers/crews.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.dependencies.db import get_db

router = APIRouter(prefix="/crews", tags=["Crews"])


@router.get("/")
async def get_all(db=Depends(get_db)):
    return {"message": "Get all crews"}


@router.get("/{item_id}")
async def get_one(item_id: str, db=Depends(get_db)):
    return {"message": f"Get crew {item_id}"}


@router.post("/")
async def create(db=Depends(get_db)):
    return {"message": "Create crew"}


@router.put("/{item_id}")
async def update(item_id: str, db=Depends(get_db)):
    return {"message": f"Update crew {item_id}"}


@router.delete("/{item_id}")
async def delete(item_id: str, db=Depends(get_db)):
    return {"message": f"Delete crew {item_id}"}
EOF

# Agents router
cat > api/routers/agents.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.dependencies.db import get_db

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("/")
async def get_all(db=Depends(get_db)):
    return {"message": "Get all agents"}


@router.get("/{item_id}")
async def get_one(item_id: str, db=Depends(get_db)):
    return {"message": f"Get agent {item_id}"}


@router.post("/")
async def create(db=Depends(get_db)):
    return {"message": "Create agent"}


@router.put("/{item_id}")
async def update(item_id: str, db=Depends(get_db)):
    return {"message": f"Update agent {item_id}"}


@router.delete("/{item_id}")
async def delete(item_id: str, db=Depends(get_db)):
    return {"message": f"Delete agent {item_id}"}
EOF

# Tasks router
cat > api/routers/tasks.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.dependencies.db import get_db

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/")
async def get_all(db=Depends(get_db)):
    return {"message": "Get all tasks"}


@router.get("/{item_id}")
async def get_one(item_id: str, db=Depends(get_db)):
    return {"message": f"Get task {item_id}"}


@router.post("/")
async def create(db=Depends(get_db)):
    return {"message": "Create task"}


@router.put("/{item_id}")
async def update(item_id: str, db=Depends(get_db)):
    return {"message": f"Update task {item_id}"}


@router.delete("/{item_id}")
async def delete(item_id: str, db=Depends(get_db)):
    return {"message": f"Delete task {item_id}"}
EOF

# Tools router
cat > api/routers/tools.py << 'EOF'
from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.dependencies.db import get_db

router = APIRouter(prefix="/tools", tags=["Tools"])


@router.get("/")
async def get_all(db=Depends(get_db)):
    return {"message": "Get all tools"}


@router.get("/{item_id}")
async def get_one(item_id: str, db=Depends(get_db)):
    return {"message": f"Get tool {item_id}"}


@router.post("/")
async def create(db=Depends(get_db)):
    return {"message": "Create tool"}


@router.put("/{item_id}")
async def update(item_id: str, db=Depends(get_db)):
    return {"message": f"Update tool {item_id}"}


@router.delete("/{item_id}")
async def delete(item_id: str, db=Depends(get_db)):
    return {"message": f"Delete tool {item_id}"}
EOF

# Create basic content for the base classes
cat > crew/agents/base_agent.py << 'EOF'
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
EOF

cat > crew/crews/base_crew.py << 'EOF'
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
EOF

cat > crew/tasks/base_task.py << 'EOF'
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
EOF

cat > crew/tools/base_tool.py << 'EOF'
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
EOF

echo "Project structure created successfully in the current directory"
echo "Next steps:"
echo "1. Configure your .env file with Supabase credentials"
echo "2. Run 'poetry install' to install dependencies"
echo "3. Start the application with 'poetry run python main.py'"
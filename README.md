# CrewAI-Local

This project implements a local version of CrewAI with Supabase integration, featuring a clean modular structure, FastAPI for the REST API, and Poetry for dependency management.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Poetry (dependency management)
- A Supabase account with credentials

### Setup after cloning

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Configure environment variables**
   Create a `.env` file in the project root with your Supabase credentials:
   ```
   SUPABASE_URL=your-supabase-url
   SUPABASE_KEY=your-supabase-api-key
   ```

3. **Run the application**
   ```bash
   poetry run python main.py
   ```
   The API will be available at http://localhost:8000

4. **Access the API documentation**
   Open your browser and navigate to http://localhost:8000/docs to explore the interactive API documentation.

## Project Structure

```
crewai-local/
│
├── api/                     # API module
│   ├── routers/             # API routes
│   ├── models/              # Pydantic models for API
│   └── dependencies/        # API dependencies
│
├── crew/                    # CrewAI module
│   ├── agents/              # Agent definitions
│   ├── crews/               # Crew definitions
│   ├── tasks/               # Task definitions
│   ├── tools/               # Tool definitions
│   └── utils/               # Utility functions
│
├── config/                  # Configuration
│
├── tests/                   # Tests
│   ├── api/                 # API tests
│   └── crew/                # CrewAI tests
│
├── main.py                  # Entry point
└── pyproject.toml           # Poetry configuration
```

## Development

### Adding new components

- **Create a new agent**: Add a new class in `crew/agents/` that inherits from `BaseAgent`
- **Create a new crew**: Add a new class in `crew/crews/` that inherits from `BaseCrew`
- **Create a new task**: Add a new class in `crew/tasks/` that inherits from `BaseTask`
- **Create a new tool**: Add a new class in `crew/tools/` that inherits from `BaseTool`

### Running tests

```bash
poetry run pytest
```

### Code formatting

```bash
poetry run black .
```

## Deployment

The project can be deployed in several ways:

1. **Directly** on a server with Python and Poetry installed
2. **As a Docker container** using the included Dockerfile (optional)
3. **On an LXC container** in Proxmox (see backup script for details)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request






# Docker Setup for CrewAI-Local

This document outlines how to use Docker with the CrewAI-Local project, including configuration details and important considerations.

## Getting Started with Docker

### Prerequisites
- Docker and Docker Compose installed on your system
- Access to your local Supabase instance (http://192.168.0.120:3000)
- Access to your local Ollama instance (http://192.168.0.201:11434)

### Configuration Steps

1. **Create your .env file**:
   ```bash
   cp .env.example .env
   ```

2. **Update the .env file** with your actual credentials:
   ```
   SUPABASE_KEY=your-actual-supabase-key
   OPENAI_API_KEY=your-actual-openai-key
   ANTHROPIC_API_KEY=your-actual-anthropic-key
   ```

3. **Build and start the Docker containers**:
   ```bash
   docker-compose up -d
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Important Configuration Notes

The `.env` file must align with `docker-compose.yml` regarding:

1. **External service URLs**: Make sure the URLs for Supabase and Ollama match your actual network configuration
2. **Database connection string**: Ensure the PostgreSQL connection string points to the correct host
3. **API keys**: All required API keys must be provided for the services you intend to use

## Network Configuration

- The Docker container needs to reach your local Supabase (192.168.0.120) and Ollama (192.168.0.201) services
- Your host machine's firewall must allow connections from Docker containers to these IPs and ports
- If running on a different network, modify the IP addresses in both `.env` and `docker-compose.yml`

## Service Configuration

### Ollama Integration

Ollama configuration is managed through these environment variables:
- `OLLAMA_API_BASE`: The base URL for your Ollama instance (http://192.168.0.201:11434)
- `OLLAMA_MODEL`: The default model to use (e.g., llama3)

You can override these in your `.env` file or when running Docker Compose:

```bash
OLLAMA_MODEL=mistral docker-compose up -d
```

### Supabase Integration

This project uses an external Supabase instance running at http://192.168.0.120:3000. No local Supabase container is needed.

## Development Workflow

1. **Code changes**: The Docker setup includes volume mounting, so code changes are reflected without rebuilding
2. **Adding dependencies**: If you add new dependencies with Poetry, rebuild the Docker image:
   ```bash
   docker-compose build --no-cache
   docker-compose up -d
   ```

3. **Debugging**: View container logs with:
   ```bash
   docker-compose logs -f app
   ```

## Troubleshooting

1. **Connection issues to Supabase or Ollama**:
   - Verify the services are running and accessible from your host machine
   - Check that Docker's network configuration allows outbound connections to your local network
   - Ensure the IP addresses in your configuration match your actual network setup

2. **Container fails to start**:
   - Check container logs: `docker-compose logs app`
   - Verify all required environment variables are set correctly
   - Make sure your Python dependencies are compatible with Python 3.10

3. **API not responding**:
   - Confirm the container is running: `docker-compose ps`
   - Check for errors in the logs: `docker-compose logs -f app`
   - Verify the port mapping is correct in docker-compose.yml (8000:8000)
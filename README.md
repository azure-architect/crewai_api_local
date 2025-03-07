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
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

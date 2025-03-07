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

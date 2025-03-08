from supabase import create_client, Client
from config.settings import settings
import os

def get_db() -> Client:
    try:
        # For better error detection
        if not settings.supabase_url or not settings.supabase_key:
            print("Supabase URL or key is missing in environment variables")
            
        # Create the client with your self-hosted configuration
        supabase = create_client(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_key,
        )
        
        # Test connection by making a simple query
        # This will fail fast if connection details are wrong
        try:
            # Just a lightweight test query
            supabase.table("any_table_name").select("*").limit(1).execute()
            print("Supabase connection successful")
        except Exception as conn_err:
            print(f"Supabase connection test failed: {conn_err}")
            # Continue anyway for now
            
        return supabase
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        # For development, return a mock or raise with better information
        raise Exception(f"Supabase connection failed. Check your URL and key format. Details: {e}")
from supabase import create_client
from config.settings import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)


def get_db():
    return supabase

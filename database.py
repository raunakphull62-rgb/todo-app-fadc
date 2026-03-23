from supabase import create_client, Client
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optional
import os

class DatabaseConfig(BaseModel):
    url: str
    key: str

class SupabaseClient:
    def __init__(self, config: DatabaseConfig):
        self.supabase_url = config.url
        self.supabase_key = config.key
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)

    def get_supabase(self) -> Client:
        return self.supabase

def get_database_config() -> DatabaseConfig:
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')

    if not supabase_url or not supabase_key:
        raise HTTPException(status_code=500, detail='Supabase URL or key not found')

    return DatabaseConfig(url=supabase_url, key=supabase_key)

def get_supabase_client() -> SupabaseClient:
    config = get_database_config()
    return SupabaseClient(config)

def get_supabase() -> Client:
    client = get_supabase_client()
    return client.get_supabase()
"""
Configuration settings for the Hotel Booking Cancellation Prediction System.
Handles environment variables and application settings.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase Configuration
    supabase_url: str
    supabase_key: str
    supabase_service_role_key: str
    
    # Database Configuration
    database_url: str
    
    # JWT Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application Configuration
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # API Configuration
    api_v1_prefix: str = "/api/v1"
    project_name: str = "Hotel Booking Cancellation Prediction System"
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Database connection string for direct PostgreSQL access
def get_database_url() -> str:
    """Get the database URL for direct PostgreSQL connection."""
    return settings.database_url

# Supabase client configuration
def get_supabase_config() -> dict:
    """Get Supabase configuration for client initialization."""
    return {
        "url": settings.supabase_url,
        "key": settings.supabase_key
    }

"""
Database connection and session management for Supabase PostgreSQL.
Handles connection pooling and database operations.
"""

import os
from typing import Optional
from supabase import create_client, Client
from app.config import settings


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self):
        self._client: Optional[Client] = None
        self._service_client: Optional[Client] = None
    
    @property
    def client(self) -> Client:
        """Get the main Supabase client for regular operations."""
        if self._client is None:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return self._client
    
    @property
    def service_client(self) -> Client:
        """Get the service role Supabase client for admin operations."""
        if self._service_client is None:
            self._service_client = create_client(
                settings.supabase_url,
                settings.supabase_service_role_key
            )
        return self._service_client
    
    async def test_connection(self) -> bool:
        """Test database connection."""
        try:
            # Simple query to test connection
            result = self.client.table("users").select("user_id").limit(1).execute()
            return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()

# Convenience functions for accessing database clients
def get_db_client() -> Client:
    """Get the main database client."""
    return db_manager.client

def get_service_client() -> Client:
    """Get the service role database client."""
    return db_manager.service_client

# Database operation helpers
class DatabaseOperations:
    """Helper class for common database operations."""
    
    @staticmethod
    def execute_query(table_name: str, operation: str, **kwargs):
        """Execute a database query with error handling."""
        try:
            client = get_db_client()
            table = client.table(table_name)
            
            if operation == "select":
                return table.select(kwargs.get("columns", "*")).execute()
            elif operation == "insert":
                return table.insert(kwargs.get("data")).execute()
            elif operation == "update":
                return table.update(kwargs.get("data")).filter(
                    kwargs.get("filter_column"), 
                    kwargs.get("filter_value")
                ).execute()
            elif operation == "delete":
                return table.delete().filter(
                    kwargs.get("filter_column"), 
                    kwargs.get("filter_value")
                ).execute()
        except Exception as e:
            print(f"Database operation failed: {e}")
            raise e

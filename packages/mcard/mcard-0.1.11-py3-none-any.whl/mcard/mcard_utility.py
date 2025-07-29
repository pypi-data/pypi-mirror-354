from typing import Optional, Dict, Any, Union, Literal
import json
import os

# Import configuration
from mcard.config.env_parameters import EnvParameters

# Import models
from mcard.model.card_collection import CardCollection
from mcard.model.card import MCard

# Import engines
from mcard.engine.base import StorageEngine, DatabaseConnection
from mcard.engine.sqlite_engine import SQLiteEngine, SQLiteConnection

# Only SQLite is supported as the database engine

class MCardUtility:
    """A utility class that simplifies working with MCard.
    
    This class provides a simplified interface for MCard operations with support
    for different database engines and configurations.
    """
    
    def __init__(self, engine=None, db_path=None, env_params=None, engine_type='sqlite'):
        """Initialize the MCardUtility with optional custom configuration.
        
        Args:
            engine: Optional custom engine to use (defaults to specified engine_type if None)
            db_path: Optional custom database path (defaults to env_params.get_db_path() if None)
            env_params: Optional custom environment parameters (defaults to EnvParameters() if None)
            engine_type: Type of database engine to use (only 'sqlite' is supported)
        """
        # Load environment parameters if not provided
        self.env_params = env_params or EnvParameters()
        
        # Create a database file path using the default configuration or provided path
        self.db_path = db_path or self.env_params.get_db_path()
        self.engine_type = engine_type.lower()
        
        # Set up the engine and card collection
        if engine is not None:
            self.engine = engine
        else:
            # Create the appropriate connection and engine based on the engine_type
            connection = self._create_connection()
            self.engine = self._create_engine(connection)
            
        self.collection = CardCollection(self.engine)
        
    def _create_connection(self) -> DatabaseConnection:
        """Create the appropriate database connection based on engine_type."""
        if self.engine_type == 'sqlite':
            return SQLiteConnection(self.db_path)

        else:
            raise ValueError(f"Unsupported engine type: {self.engine_type}. "
                           f"Supported types are 'sqlite', 'duckdb'.")
            
    def _create_engine(self, connection: DatabaseConnection) -> StorageEngine:
        """Create the appropriate storage engine based on engine_type."""
        if self.engine_type == 'sqlite':
            return SQLiteEngine(connection)

        else:
            raise ValueError(f"Unsupported engine type: {self.engine_type}. "
                           f"Supported types are 'sqlite', 'duckdb'.")

    def add_card(self, content: Union[str, Dict[str, Any]]) -> str:
        """Add a card with the provided content.
        
        Args:
            content: String content or dictionary that will be converted to JSON
            
        Returns:
            The hash of the added card
        """
        # Convert dict to JSON if needed
        if isinstance(content, dict):
            content = json.dumps(content)
            
        card = MCard(content=content)
        self.collection.add(card)
        return card.hash

    def get_card(self, hash_value: str) -> Optional[MCard]:
        """Retrieve a card by its hash.
        
        Args:
            hash_value: The hash of the card to retrieve
            
        Returns:
            The MCard if found, None otherwise
        """
        return self.collection.get(hash_value)

    def delete_card(self, hash_value: str) -> bool:
        """Delete a card by its hash.
        
        Args:
            hash_value: The hash of the card to delete
            
        Returns:
            True if the card was deleted, False otherwise
        """
        return self.collection.delete(hash_value)

    def get_collection(self) -> CardCollection:
        """Get the underlying card collection.
        
        Returns:
            The CardCollection instance
        """
        return self.collection
        
    def search(self, query: str, page: int = 1, page_size: int = 10) -> list:
        """Search for cards using the provided query.
        
        Args:
            query: The search query string
            page: The page number (starting from 1)
            page_size: The number of items per page
            
        Returns:
            A list of matching cards
        """
        return self.collection.search_by_string(query, page, page_size)

"""Core PostgreSQL operations module."""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union
import psycopg2
from psycopg2.extras import RealDictCursor

from .exceptions import ConnectionError, QueryError
from .config_loader import load_from_env, validate_config

# Configure logging
logger = logging.getLogger(__name__)

class PostgresOps:
    """A lightweight PostgreSQL operations manager."""
    
    def __init__(self, config: Dict[str, str], logging_enabled: bool = False):
        """
        Initialize PostgreSQL operations manager.
        
        Args:
            config: PostgreSQL configuration dictionary
            logging_enabled: Enable logging for database operations
        """
        self.logging_enabled = logging_enabled
        if self.logging_enabled:
            logger.info("Initializing PostgreSQL operations")
        
        validate_config(config, logging_enabled)
        self.config = config
        self._conn = None
    
    @classmethod
    def from_env(cls, env_prefix: str = "DB_", logging_enabled: bool = False) -> 'PostgresOps':
        """
        Create instance from environment variables.
        
        Args:
            env_prefix: Prefix for environment variables
            logging_enabled: Enable logging for database operations
        
        Returns:
            PostgresOps instance
        """
        config = load_from_env(env_prefix, logging_enabled)
        return cls(config, logging_enabled)
    
    @classmethod
    def from_config(cls, config: Dict[str, str], logging_enabled: bool = False) -> 'PostgresOps':
        """
        Create instance from configuration dictionary.
        
        Args:
            config: PostgreSQL configuration dictionary
            logging_enabled: Enable logging for database operations
        
        Returns:
            PostgresOps instance
        """
        return cls(config, logging_enabled)
    
    def _get_connection(self):
        """Get or create database connection."""
        try:
            if self._conn is None or self._conn.closed:
                if self.logging_enabled:
                    logger.debug("Creating new database connection")
                self._conn = psycopg2.connect(**self.config)
            return self._conn
        except psycopg2.Error as e:
            error_msg = f"Failed to connect to PostgreSQL: {str(e)}"
            if self.logging_enabled:
                logger.error(error_msg)
            raise ConnectionError(error_msg)
    
    def fetch(
        self,
        query: str,
        params: Optional[List[Any]] = None,
        as_dict: bool = True
    ) -> List[Union[Dict[str, Any], Tuple]]:
        """
        Execute a SELECT query and fetch all results.
        
        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
            as_dict: Return results as dictionaries (default: True)
        
        Returns:
            List of query results
        
        Raises:
            QueryError: If query execution fails
        """
        if self.logging_enabled:
            logger.info("Executing fetch query")
            logger.debug("Query: %s, Params: %s", query, params)
        
        conn = self._get_connection()
        cursor_factory = RealDictCursor if as_dict else None
        
        try:
            with conn.cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query, params)
                results = cur.fetchall()
                
                if self.logging_enabled:
                    logger.info("Query executed successfully")
                    logger.debug("Results: %s", results)
                
                return results
        except psycopg2.Error as e:
            error_msg = f"Query execution failed: {str(e)}"
            if self.logging_enabled:
                logger.error(error_msg)
            conn.rollback()
            raise QueryError(error_msg)
    
    def execute(
        self,
        query: str,
        params: Optional[List[Any]] = None
    ) -> int:
        """
        Execute a modification query (INSERT, UPDATE, DELETE).
        
        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
        
        Returns:
            Number of affected rows
        
        Raises:
            QueryError: If query execution fails
        """
        if self.logging_enabled:
            logger.info("Executing modification query")
            logger.debug("Query: %s, Params: %s", query, params)
        
        conn = self._get_connection()
        
        try:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                affected_rows = cur.rowcount
                
                if self.logging_enabled:
                    logger.info("Query executed successfully")
                    logger.debug("Affected rows: %d", affected_rows)
                
                return affected_rows
        except psycopg2.Error as e:
            error_msg = f"Query execution failed: {str(e)}"
            if self.logging_enabled:
                logger.error(error_msg)
            conn.rollback()
            raise QueryError(error_msg)
    
    def close(self) -> None:
        """Close database connection."""
        if self._conn is not None and not self._conn.closed:
            if self.logging_enabled:
                logger.info("Closing database connection")
            try:
                self._conn.close()
            finally:
                self._conn = None 
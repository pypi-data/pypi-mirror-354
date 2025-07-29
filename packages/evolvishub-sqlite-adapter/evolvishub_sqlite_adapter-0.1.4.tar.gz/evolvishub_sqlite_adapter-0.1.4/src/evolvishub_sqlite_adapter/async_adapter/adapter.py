"""
Async SQLite adapter implementation.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Union, Set

import aiosqlite
import sqlite3

from ..config import DatabaseConfig
from ..utils.exceptions import (
    ConnectionError,
    QueryError,
    TransactionError,
    PoolError,
)


class AsyncSQLiteAdapter:
    """
    Asynchronous SQLite adapter with connection pooling and transaction support.
    
    Attributes:
        config (DatabaseConfig): Database configuration
        _pool (asyncio.Queue): Connection pool
        _logger (logging.Logger): Logger instance
        _transaction_connections (Set[aiosqlite.Connection]): Set of connections in transaction
    """
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize the async SQLite adapter.
        
        Args:
            config (DatabaseConfig): Database configuration
        """
        self.config = config
        self._pool: Optional[asyncio.Queue] = None
        self._logger = self._setup_logger()
        self._transaction_connections: Set[aiosqlite.Connection] = set()
        self._current_transaction_conn: Optional[aiosqlite.Connection] = None
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with the configured settings."""
        logger = logging.getLogger("evolvishub_sqlite_adapter")
        logger.setLevel(self.config.log_level.upper())
        
        if self.config.log_file:
            handler = logging.FileHandler(self.config.log_file)
        else:
            handler = logging.StreamHandler()
        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    async def connect(self) -> None:
        """Initialize the connection pool."""
        try:
            self._pool = asyncio.Queue(maxsize=self.config.pool_size)
            for _ in range(self.config.pool_size):
                conn = await aiosqlite.connect(
                    self.config.database,
                    check_same_thread=self.config.check_same_thread,
                )
                await conn.execute(f"PRAGMA journal_mode = {self.config.journal_mode}")
                await conn.execute(f"PRAGMA synchronous = {self.config.synchronous}")
                await conn.execute(f"PRAGMA foreign_keys = {'ON' if self.config.foreign_keys else 'OFF'}")
                await conn.execute(f"PRAGMA cache_size = {self.config.cache_size}")
                await conn.execute(f"PRAGMA temp_store = {self.config.temp_store}")
                await conn.execute(f"PRAGMA page_size = {self.config.page_size}")
                await self._pool.put(conn)
            
            self._logger.info(f"Initialized connection pool with {self.config.pool_size} connections")
        except Exception as e:
            raise ConnectionError(f"Failed to initialize connection pool: {str(e)}")
    
    async def close(self) -> None:
        """Close all connections in the pool."""
        if not self._pool:
            return
        
        while not self._pool.empty():
            conn = await self._pool.get()
            await conn.close()
        
        self._logger.info("Closed all database connections")
        self._pool = None
        self._transaction_connections.clear()
        self._current_transaction_conn = None
    
    @asynccontextmanager
    async def _get_connection(self):
        """Get a connection from the pool."""
        if not self._pool:
            raise PoolError("Connection pool not initialized")
        
        # If we're in a transaction, use the same connection
        if self._current_transaction_conn is not None:
            yield self._current_transaction_conn
            return
        
        try:
            # Check if we've reached the pool size limit
            if len(self._pool._getters) >= self.config.pool_size:
                raise PoolError("Connection pool exhausted")
                
            conn = await asyncio.wait_for(self._pool.get(), timeout=1.0)
            try:
                yield conn
            finally:
                if conn not in self._transaction_connections:
                    await self._pool.put(conn)
        except asyncio.TimeoutError:
            raise PoolError("Connection pool exhausted")
    
    async def execute(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> None:
        """
        Execute a query without returning results.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
        """
        if not query:
            raise ValueError("Query cannot be empty")

        try:
            async with self._get_connection() as conn:
                await conn.execute(query, params or ())
                if conn not in self._transaction_connections:
                    await conn.commit()
        except sqlite3.Error as e:
            raise QueryError(f"Failed to execute query: {str(e)}")
        except Exception as e:
            if self._current_transaction_conn is not None:
                raise TransactionError(f"Transaction failed: {str(e)}")
            raise
    
    async def fetch_one(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch a single row from the database.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
            
        Returns:
            Optional[Dict[str, Any]]: Row as dictionary or None if no results
        """
        try:
            async with self._get_connection() as conn:
                async with conn.execute(query, params or ()) as cursor:
                    row = await cursor.fetchone()
                    if row:
                        return dict(zip([col[0] for col in cursor.description], row))
                    return None
        except Exception as e:
            raise QueryError(f"Failed to fetch one: {str(e)}")
    
    async def fetch_all(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch all rows from the database.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
            
        Returns:
            List[Dict[str, Any]]: List of rows as dictionaries
        """
        try:
            async with self._get_connection() as conn:
                async with conn.execute(query, params or ()) as cursor:
                    rows = await cursor.fetchall()
                    return [
                        dict(zip([col[0] for col in cursor.description], row))
                        for row in rows
                    ]
        except Exception as e:
            raise QueryError(f"Failed to fetch all: {str(e)}")
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        if self._current_transaction_conn is not None:
            raise TransactionError("Nested transactions are not supported")
        
        async with self._get_connection() as conn:
            try:
                self._current_transaction_conn = conn
                await conn.execute("BEGIN")
                self._transaction_connections.add(conn)
                yield
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                if isinstance(e, TransactionError):
                    raise
                raise TransactionError(f"Transaction failed: {str(e)}")
            finally:
                self._current_transaction_conn = None
                self._transaction_connections.remove(conn)

    async def disconnect(self) -> None:
        """Alias for close() method."""
        await self.close()

    async def count_rows(
        self,
        table_name: str,
        where_clause: Optional[str] = None,
        params: Optional[Union[tuple, dict]] = None
    ) -> int:
        """
        Count the number of rows in a table with optional filtering.
        
        Args:
            table_name (str): Name of the table to count rows from
            where_clause (Optional[str]): Optional WHERE clause for filtering
            params (Optional[Union[tuple, dict]]): Parameters for the WHERE clause
            
        Returns:
            int: Number of rows matching the criteria
        """
        if not table_name:
            raise ValueError("Table name cannot be empty")
            
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
            
        try:
            result = await self.fetch_one(query, params)
            return result["count"] if result else 0
        except Exception as e:
            raise QueryError(f"Failed to count rows: {str(e)}")

    async def delete_data(
        self,
        table_name: str,
        where_clause: Optional[str] = None,
        params: Optional[Union[tuple, dict]] = None
    ) -> int:
        """
        Delete data from a table with optional filtering.
        
        Args:
            table_name (str): Name of the table to delete from
            where_clause (Optional[str]): Optional WHERE clause for filtering
            params (Optional[Union[tuple, dict]]): Parameters for the WHERE clause
            
        Returns:
            int: Number of rows deleted
        """
        if not table_name:
            raise ValueError("Table name cannot be empty")
            
        query = f"DELETE FROM {table_name}"
        if where_clause:
            query += f" WHERE {where_clause}"
            
        try:
            async with self._get_connection() as conn:
                cursor = await conn.execute(query, params or ())
                if conn not in self._transaction_connections:
                    await conn.commit()
                return cursor.rowcount
        except Exception as e:
            raise QueryError(f"Failed to delete data: {str(e)}")

    async def execute_raw(
        self,
        query: str,
        params: Optional[Union[tuple, dict]] = None
    ) -> Any:
        """
        Execute a raw SQL query and return the cursor.
        
        Args:
            query (str): SQL query to execute
            params (Optional[Union[tuple, dict]]): Query parameters
            
        Returns:
            Any: The result of the query execution
        """
        if not query:
            raise ValueError("Query cannot be empty")
            
        try:
            async with self._get_connection() as conn:
                cursor = await conn.execute(query, params or ())
                if conn not in self._transaction_connections:
                    await conn.commit()
                return cursor
        except Exception as e:
            raise QueryError(f"Failed to execute raw query: {str(e)}")

    async def get_row_by_id(
        self,
        table_name: str,
        id_value: Any,
        id_column: str = "id"
    ) -> Optional[Dict[str, Any]]:
        """
        Get a single row from a table by its ID.
        
        Args:
            table_name (str): Name of the table to query
            id_value (Any): Value of the ID to look up
            id_column (str): Name of the ID column (defaults to "id")
            
        Returns:
            Optional[Dict[str, Any]]: Row as dictionary or None if not found
        """
        if not table_name:
            raise ValueError("Table name cannot be empty")
            
        query = f"SELECT * FROM {table_name} WHERE {id_column} = ?"
        return await self.fetch_one(query, (id_value,))

    async def get_table_names(self) -> List[str]:
        """
        Get a list of all table names in the database.
        
        Returns:
            List[str]: List of table names
        """
        try:
            results = await self.fetch_all(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            return [row["name"] for row in results]
        except Exception as e:
            raise QueryError(f"Failed to get table names: {str(e)}")

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close() 
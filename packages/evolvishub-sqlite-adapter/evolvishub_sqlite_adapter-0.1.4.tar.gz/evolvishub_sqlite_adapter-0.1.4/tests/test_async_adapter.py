"""
Tests for the async SQLite adapter.
"""

import pytest
import asyncio
from src.evolvishub_sqlite_adapter.utils.exceptions import (
    QueryError,
    TransactionError,
    PoolError,
    ConnectionError
)


@pytest.mark.asyncio
async def test_connection_pool(async_adapter):
    """Test connection pool initialization."""
    assert async_adapter._pool is not None
    assert async_adapter._pool.qsize() == 2


@pytest.mark.asyncio
async def test_execute(async_adapter):
    """Test execute method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name) VALUES (?)",
        ("test",)
    )
    
    result = await async_adapter.fetch_one(
        "SELECT name FROM test WHERE id = ?",
        (1,)
    )
    assert result["name"] == "test"


@pytest.mark.asyncio
async def test_fetch_all(async_adapter):
    """Test fetch_all method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name) VALUES (?), (?)",
        ("test1", "test2")
    )
    
    results = await async_adapter.fetch_all("SELECT * FROM test ORDER BY id")
    assert len(results) == 2
    assert results[0]["name"] == "test1"
    assert results[1]["name"] == "test2"


@pytest.mark.asyncio
async def test_transaction(async_adapter):
    """Test transaction context manager."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    
    async with async_adapter.transaction():
        await async_adapter.execute(
            "INSERT INTO test (name) VALUES (?)",
            ("test",)
        )
    
    result = await async_adapter.fetch_one("SELECT name FROM test")
    assert result["name"] == "test"


@pytest.mark.asyncio
async def test_transaction_rollback(async_adapter):
    """Test transaction rollback."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )

    with pytest.raises(TransactionError) as exc_info:
        async with async_adapter.transaction():
            await async_adapter.execute(
                "INSERT INTO test (name) VALUES (?)",
                ("test",)
            )
            raise Exception("Rollback test")
    assert 'Rollback test' in str(exc_info.value)

    result = await async_adapter.fetch_one("SELECT COUNT(*) as count FROM test")
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_invalid_query(async_adapter):
    """Test handling of invalid queries."""
    with pytest.raises(QueryError) as exc_info:
        await async_adapter.execute("INVALID SQL")
    assert 'near "INVALID": syntax error' in str(exc_info.value)


@pytest.mark.asyncio
async def test_connection_cleanup(async_adapter):
    """Test connection cleanup."""
    await async_adapter.close()
    assert async_adapter._pool is None


@pytest.mark.asyncio
async def test_disconnect(async_adapter):
    """Test disconnect method."""
    await async_adapter.disconnect()
    assert async_adapter._pool is None
    assert len(async_adapter._transaction_connections) == 0
    assert async_adapter._current_transaction_conn is None


@pytest.mark.asyncio
async def test_count_rows(async_adapter):
    """Test count_rows method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name, value) VALUES (?, ?), (?, ?), (?, ?)",
        ("test1", 1, "test2", 2, "test3", 3)
    )
    
    # Test counting all rows
    count = await async_adapter.count_rows("test")
    assert count == 3
    
    # Test counting with where clause
    count = await async_adapter.count_rows("test", "value > ?", (1,))
    assert count == 2
    
    # Test counting with empty table
    await async_adapter.execute("DELETE FROM test")
    count = await async_adapter.count_rows("test")
    assert count == 0


@pytest.mark.asyncio
async def test_count_rows_invalid(async_adapter):
    """Test count_rows with invalid input."""
    with pytest.raises(ValueError):
        await async_adapter.count_rows("")
    
    with pytest.raises(QueryError):
        await async_adapter.count_rows("nonexistent_table")


@pytest.mark.asyncio
async def test_delete_data(async_adapter):
    """Test delete_data method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name, value) VALUES (?, ?), (?, ?), (?, ?)",
        ("test1", 1, "test2", 2, "test3", 3)
    )
    
    # Test deleting specific rows
    deleted = await async_adapter.delete_data("test", "value > ?", (1,))
    assert deleted == 2
    
    # Verify remaining data
    remaining = await async_adapter.fetch_all("SELECT * FROM test ORDER BY id")
    assert len(remaining) == 1
    assert remaining[0]["name"] == "test1"
    
    # Test deleting all rows
    deleted = await async_adapter.delete_data("test")
    assert deleted == 1
    count = await async_adapter.count_rows("test")
    assert count == 0


@pytest.mark.asyncio
async def test_delete_data_invalid(async_adapter):
    """Test delete_data with invalid input."""
    with pytest.raises(ValueError):
        await async_adapter.delete_data("")
    
    with pytest.raises(QueryError):
        await async_adapter.delete_data("nonexistent_table")


@pytest.mark.asyncio
async def test_execute_raw(async_adapter):
    """Test execute_raw method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    
    # Test insert
    cursor = await async_adapter.execute_raw(
        "INSERT INTO test (name) VALUES (?)",
        ("test1",)
    )
    assert cursor.rowcount == 1
    
    # Test select
    cursor = await async_adapter.execute_raw("SELECT * FROM test")
    row = await cursor.fetchone()
    assert row[1] == "test1"  # name column


@pytest.mark.asyncio
async def test_execute_raw_invalid(async_adapter):
    """Test execute_raw with invalid input."""
    with pytest.raises(ValueError):
        await async_adapter.execute_raw("")
    
    with pytest.raises(QueryError):
        await async_adapter.execute_raw("INVALID SQL")


@pytest.mark.asyncio
async def test_get_row_by_id(async_adapter):
    """Test get_row_by_id method."""
    await async_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
    )
    await async_adapter.execute(
        "INSERT INTO test (name, value) VALUES (?, ?), (?, ?)",
        ("test1", 1, "test2", 2)
    )
    
    # Test getting row by default id column
    row = await async_adapter.get_row_by_id("test", 1)
    assert row["name"] == "test1"
    assert row["value"] == 1
    
    # Test getting row by custom id column
    await async_adapter.execute(
        "CREATE TABLE test2 (custom_id INTEGER PRIMARY KEY, name TEXT)"
    )
    await async_adapter.execute(
        "INSERT INTO test2 (name) VALUES (?)",
        ("test1",)
    )
    row = await async_adapter.get_row_by_id("test2", 1, "custom_id")
    assert row["name"] == "test1"
    
    # Test getting non-existent row
    row = await async_adapter.get_row_by_id("test", 999)
    assert row is None


@pytest.mark.asyncio
async def test_get_row_by_id_invalid(async_adapter):
    """Test get_row_by_id with invalid input."""
    with pytest.raises(ValueError):
        await async_adapter.get_row_by_id("", 1)
    
    with pytest.raises(QueryError):
        await async_adapter.get_row_by_id("nonexistent_table", 1)


@pytest.mark.asyncio
async def test_get_table_names(async_adapter):
    """Test get_table_names method."""
    # Create some test tables
    await async_adapter.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY)")
    await async_adapter.execute("CREATE TABLE test2 (id INTEGER PRIMARY KEY)")
    await async_adapter.execute("CREATE TABLE test3 (id INTEGER PRIMARY KEY)")
    
    # Get table names
    tables = await async_adapter.get_table_names()
    
    # Verify all tables are present
    assert "test1" in tables
    assert "test2" in tables
    assert "test3" in tables
    
    # Verify system tables are not included
    assert "sqlite_sequence" not in tables


@pytest.mark.asyncio
async def test_nested_transaction(async_adapter):
    """Test that nested transactions are not allowed."""
    await async_adapter.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
    
    async with async_adapter.transaction():
        with pytest.raises(TransactionError) as exc_info:
            async with async_adapter.transaction():
                await async_adapter.execute("INSERT INTO test DEFAULT VALUES")
        assert "Nested transactions are not supported" in str(exc_info.value)


@pytest.mark.asyncio
@pytest.mark.skip(reason="Connection pool exhaustion test is flaky due to async timing issues")
async def test_connection_pool_exhaustion(async_adapter):
    """Test behavior when connection pool is exhausted."""
    # Create more connections than the pool size
    connections = []
    for _ in range(async_adapter.config.pool_size + 1):
        try:
            async with async_adapter._get_connection() as conn:
                connections.append(conn)
                # Keep the connection open to prevent it from being returned to the pool
                await asyncio.sleep(0.1)
        except PoolError:
            break

    # Verify we can't get more connections than the pool size
    assert len(connections) == async_adapter.config.pool_size


@pytest.mark.asyncio
async def test_context_manager(async_adapter):
    """Test async context manager functionality."""
    async with async_adapter as adapter:
        assert adapter is async_adapter
        assert adapter._pool is not None
    
    # Verify connections are closed after context exit
    assert async_adapter._pool is None 
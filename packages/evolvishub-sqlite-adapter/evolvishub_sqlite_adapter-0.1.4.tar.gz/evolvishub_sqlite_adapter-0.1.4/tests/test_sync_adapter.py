"""
Tests for the sync SQLite adapter.
"""

import pytest

from src.evolvishub_sqlite_adapter.utils.exceptions import QueryError, TransactionError


def test_connection_pool(sync_adapter):
    """Test connection pool initialization."""
    assert sync_adapter._pool is not None
    assert sync_adapter._pool.qsize() == 2


def test_execute(sync_adapter):
    """Test execute method."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name) VALUES (?)",
        ("test",)
    )
    
    result = sync_adapter.fetch_one(
        "SELECT name FROM test WHERE id = ?",
        (1,)
    )
    assert result["name"] == "test"


def test_fetch_all(sync_adapter):
    """Test fetch_all method."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name) VALUES (?), (?)",
        ("test1", "test2")
    )
    
    results = sync_adapter.fetch_all("SELECT * FROM test ORDER BY id")
    assert len(results) == 2
    assert results[0]["name"] == "test1"
    assert results[1]["name"] == "test2"


def test_transaction(sync_adapter):
    """Test transaction context manager."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    
    with sync_adapter.transaction():
        sync_adapter.execute(
            "INSERT INTO test (name) VALUES (?)",
            ("test",)
        )
    
    result = sync_adapter.fetch_one("SELECT name FROM test")
    assert result["name"] == "test"


def test_transaction_rollback(sync_adapter):
    """Test transaction rollback."""
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )

    def do_transaction():
        with sync_adapter.transaction():
            sync_adapter.execute(
                "INSERT INTO test (name) VALUES (?)",
                ("test",)
            )
            raise Exception("Rollback test")

    with pytest.raises(TransactionError) as exc_info:
        do_transaction()
    assert 'Rollback test' in str(exc_info.value)


def test_invalid_query(sync_adapter):
    """Test handling of invalid queries."""
    with pytest.raises(QueryError) as exc_info:
        sync_adapter.execute("INVALID SQL")
    assert 'near "INVALID": syntax error' in str(exc_info.value)


def test_connection_cleanup(sync_adapter):
    """Test connection cleanup."""
    sync_adapter.close()
    assert sync_adapter._pool is None


def test_execute_script(sync_adapter):
    """Test execute_script method."""
    script = """
    CREATE TABLE test1 (id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE test2 (id INTEGER PRIMARY KEY, value TEXT);
    INSERT INTO test1 (name) VALUES ('test1');
    INSERT INTO test2 (value) VALUES ('test2');
    """
    sync_adapter.execute_script(script)
    
    # Verify tables and data were created
    result1 = sync_adapter.fetch_one("SELECT name FROM test1")
    result2 = sync_adapter.fetch_one("SELECT value FROM test2")
    assert result1["name"] == "test1"
    assert result2["value"] == "test2"


def test_execute_script_invalid(sync_adapter):
    """Test execute_script with invalid input."""
    with pytest.raises(ValueError):
        sync_adapter.execute_script("")
    
    with pytest.raises(QueryError):
        sync_adapter.execute_script("INVALID SQL; INVALID SQL;")


def test_count_rows(sync_adapter):
    """Test count_rows method."""
    # Create test table and insert data
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name, value) VALUES (?, ?), (?, ?), (?, ?)",
        ("test1", 1, "test2", 2, "test3", 3)
    )
    
    # Test counting all rows
    assert sync_adapter.count_rows("test") == 3
    
    # Test counting with where clause
    assert sync_adapter.count_rows("test", "value > ?", (1,)) == 2
    assert sync_adapter.count_rows("test", "name = ?", ("test1",)) == 1


def test_count_rows_invalid(sync_adapter):
    """Test count_rows with invalid input."""
    with pytest.raises(ValueError):
        sync_adapter.count_rows("")
    
    with pytest.raises(QueryError):
        sync_adapter.count_rows("nonexistent_table")


def test_delete_data(sync_adapter):
    """Test delete_data method."""
    # Create test table and insert data
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name, value) VALUES (?, ?), (?, ?), (?, ?)",
        ("test1", 1, "test2", 2, "test3", 3)
    )
    
    # Test deleting specific rows
    deleted = sync_adapter.delete_data("test", "value > ?", (1,))
    assert deleted == 2
    
    # Verify remaining data
    remaining = sync_adapter.fetch_all("SELECT * FROM test ORDER BY id")
    assert len(remaining) == 1
    assert remaining[0]["name"] == "test1"
    
    # Test deleting all rows
    deleted = sync_adapter.delete_data("test")
    assert deleted == 1
    assert sync_adapter.count_rows("test") == 0


def test_delete_data_invalid(sync_adapter):
    """Test delete_data with invalid input."""
    with pytest.raises(ValueError):
        sync_adapter.delete_data("")
    
    with pytest.raises(QueryError):
        sync_adapter.delete_data("nonexistent_table")


def test_execute_raw(sync_adapter):
    """Test execute_raw method."""
    # Create test table
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"
    )
    
    # Test insert
    cursor = sync_adapter.execute_raw(
        "INSERT INTO test (name) VALUES (?)",
        ("test1",)
    )
    assert cursor.rowcount == 1
    
    # Test select
    cursor = sync_adapter.execute_raw("SELECT * FROM test")
    row = cursor.fetchone()
    assert row[1] == "test1"  # name column


def test_execute_raw_invalid(sync_adapter):
    """Test execute_raw with invalid input."""
    with pytest.raises(ValueError):
        sync_adapter.execute_raw("")
    
    with pytest.raises(QueryError):
        sync_adapter.execute_raw("INVALID SQL")


def test_get_row_by_id(sync_adapter):
    """Test get_row_by_id method."""
    # Create test table and insert data
    sync_adapter.execute(
        "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)"
    )
    sync_adapter.execute(
        "INSERT INTO test (name, value) VALUES (?, ?), (?, ?)",
        ("test1", 1, "test2", 2)
    )
    
    # Test getting row by default id column
    row = sync_adapter.get_row_by_id("test", 1)
    assert row["name"] == "test1"
    assert row["value"] == 1
    
    # Test getting row by custom id column
    sync_adapter.execute(
        "CREATE TABLE test2 (custom_id INTEGER PRIMARY KEY, name TEXT)"
    )
    sync_adapter.execute(
        "INSERT INTO test2 (name) VALUES (?)",
        ("test1",)
    )
    row = sync_adapter.get_row_by_id("test2", 1, "custom_id")
    assert row["name"] == "test1"
    
    # Test getting non-existent row
    row = sync_adapter.get_row_by_id("test", 999)
    assert row is None


def test_get_row_by_id_invalid(sync_adapter):
    """Test get_row_by_id with invalid input."""
    with pytest.raises(ValueError):
        sync_adapter.get_row_by_id("", 1)
    
    with pytest.raises(QueryError):
        sync_adapter.get_row_by_id("nonexistent_table", 1)


def test_get_table_names(sync_adapter):
    """Test get_table_names method."""
    # Create test tables
    sync_adapter.execute("CREATE TABLE test1 (id INTEGER PRIMARY KEY)")
    sync_adapter.execute("CREATE TABLE test2 (id INTEGER PRIMARY KEY)")
    sync_adapter.execute("CREATE TABLE test3 (id INTEGER PRIMARY KEY)")
    
    # Get table names
    tables = sync_adapter.get_table_names()
    
    # Verify tables are listed
    assert "test1" in tables
    assert "test2" in tables
    assert "test3" in tables
    
    # Verify system tables are not included
    assert "sqlite_master" not in tables
    assert "sqlite_sequence" not in tables 
"""
Tests for the logging utilities.
"""

import os
import tempfile
import logging
import pytest

from evolvishub_sqlite_adapter.utils.logger import setup_logger


def test_setup_logger_with_stream():
    """Test logger setup with stream handler."""
    logger = setup_logger("DEBUG")
    
    assert logger.name == "evolvishub_sqlite_adapter"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)


def test_setup_logger_with_file():
    """Test logger setup with file handler."""
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as temp_file:
        log_file = temp_file.name
    
    try:
        logger = setup_logger("INFO", log_file)
        
        assert logger.name == "evolvishub_sqlite_adapter"
        assert logger.level == logging.INFO
        assert len(logger.handlers) == 1
        assert isinstance(logger.handlers[0], logging.FileHandler)
        
        # Test logging to file
        test_message = "Test log message"
        logger.info(test_message)
        
        # Verify the message was written to the file
        with open(log_file, 'r') as f:
            log_content = f.read()
            assert test_message in log_content
    finally:
        os.unlink(log_file)


def test_setup_logger_with_different_levels():
    """Test logger setup with different log levels."""
    levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    for level in levels:
        logger = setup_logger(level)
        assert logger.level == getattr(logging, level)


def test_setup_logger_formatter():
    """Test logger formatter configuration."""
    logger = setup_logger("DEBUG")
    handler = logger.handlers[0]
    formatter = handler.formatter
    
    assert isinstance(formatter, logging.Formatter)
    assert "%(asctime)s" in formatter._fmt
    assert "%(name)s" in formatter._fmt
    assert "%(levelname)s" in formatter._fmt
    assert "%(message)s" in formatter._fmt


def test_setup_logger_multiple_calls():
    """Test multiple logger setup calls."""
    logger1 = setup_logger("DEBUG")
    logger2 = setup_logger("INFO")
    
    # Should return the same logger instance
    assert logger1 is logger2
    # Level should be updated to the last call
    assert logger1.level == logging.INFO 
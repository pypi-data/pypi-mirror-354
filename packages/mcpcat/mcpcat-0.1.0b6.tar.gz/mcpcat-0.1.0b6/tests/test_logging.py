"""Tests for the logging module."""

import os
import time
from pathlib import Path

import pytest

from mcpcat.modules.constants import LOG_PATH
from mcpcat.modules.logging import write_to_log


class TestLogging:
    """Test the logging functionality."""

    def test_write_to_log_creates_file(self, tmp_path):
        """Test that write_to_log creates the log file if it doesn't exist."""
        # Use a temporary directory for the test
        log_file = tmp_path / "test_mcpcat.log"
        
        # Monkey patch the LOG_PATH constant
        import mcpcat.modules.logging
        original_log_path = mcpcat.modules.logging.LOG_PATH
        mcpcat.modules.logging.LOG_PATH = str(log_file)
        
        try:
            # Write a test message
            test_message = "Test log message"
            write_to_log(test_message)
            
            # Check that the file was created
            assert log_file.exists(), "Log file was not created"
            
            # Read the file content
            content = log_file.read_text()
            
            # Verify the message is in the file
            assert test_message in content, "Log message not found in file"
            
            # Verify timestamp format (ISO format)
            assert "T" in content, "Timestamp not in ISO format"
            
        finally:
            # Restore original LOG_PATH
            mcpcat.modules.logging.LOG_PATH = original_log_path

    def test_write_to_log_appends_messages(self, tmp_path):
        """Test that write_to_log appends to existing log file."""
        # Use a temporary directory for the test
        log_file = tmp_path / "test_mcpcat.log"
        
        # Monkey patch the LOG_PATH constant
        import mcpcat.modules.logging
        original_log_path = mcpcat.modules.logging.LOG_PATH
        mcpcat.modules.logging.LOG_PATH = str(log_file)
        
        try:
            # Write multiple messages
            messages = ["First message", "Second message", "Third message"]
            for msg in messages:
                write_to_log(msg)
                time.sleep(0.01)  # Small delay to ensure different timestamps
            
            # Read the file content
            content = log_file.read_text()
            lines = content.strip().split('\n')
            
            # Verify all messages are present
            assert len(lines) >= len(messages), f"Expected {len(messages)} lines, got {len(lines)}"
            
            for i, msg in enumerate(messages):
                assert msg in lines[i], f"Message '{msg}' not found in line {i}"
            
            # Verify messages are in chronological order
            timestamps = []
            for line in lines:
                # Extract timestamp from [timestamp] format
                timestamp = line.split('] ')[0].strip('[')
                timestamps.append(timestamp)
            
            # Check timestamps are in ascending order
            assert timestamps == sorted(timestamps), "Log entries are not in chronological order"
            
        finally:
            # Restore original LOG_PATH
            mcpcat.modules.logging.LOG_PATH = original_log_path

    def test_write_to_log_handles_directory_creation(self, tmp_path):
        """Test that write_to_log creates parent directories if needed."""
        # Use a nested directory structure
        log_file = tmp_path / "nested" / "dirs" / "test_mcpcat.log"
        
        # Monkey patch the LOG_PATH constant
        import mcpcat.modules.logging
        original_log_path = mcpcat.modules.logging.LOG_PATH
        mcpcat.modules.logging.LOG_PATH = str(log_file)
        
        try:
            # Write a test message
            test_message = "Test with directory creation"
            write_to_log(test_message)
            
            # Check that the directories and file were created
            assert log_file.exists(), "Log file was not created in nested directory"
            assert test_message in log_file.read_text(), "Message not written to file"
            
        finally:
            # Restore original LOG_PATH
            mcpcat.modules.logging.LOG_PATH = original_log_path

    def test_write_to_log_silently_handles_errors(self, tmp_path, monkeypatch):
        """Test that write_to_log doesn't raise exceptions on errors."""
        # Use a file that can't be written to
        log_file = tmp_path / "test_mcpcat.log"
        
        # Monkey patch the LOG_PATH constant
        import mcpcat.modules.logging
        original_log_path = mcpcat.modules.logging.LOG_PATH
        mcpcat.modules.logging.LOG_PATH = str(log_file)
        
        try:
            # Make the parent directory read-only to cause write failure
            log_file.parent.chmod(0o444)
            
            # This should not raise an exception
            write_to_log("This should fail silently")
            
            # If we get here without exception, the test passes
            assert True
            
        finally:
            # Restore permissions and original LOG_PATH
            log_file.parent.chmod(0o755)
            mcpcat.modules.logging.LOG_PATH = original_log_path

    def test_log_format(self, tmp_path):
        """Test the format of log entries."""
        # Use a temporary directory for the test
        log_file = tmp_path / "test_mcpcat.log"
        
        # Monkey patch the LOG_PATH constant
        import mcpcat.modules.logging
        original_log_path = mcpcat.modules.logging.LOG_PATH
        mcpcat.modules.logging.LOG_PATH = str(log_file)
        
        try:
            # Write a test message
            test_message = "Test format validation"
            write_to_log(test_message)
            
            # Read the log entry
            content = log_file.read_text().strip()
            
            # Verify format: "[ISO_TIMESTAMP] MESSAGE"
            assert content.startswith('['), "Log entry should start with ["
            assert '] ' in content, "Log entry should have timestamp in brackets followed by space"
            
            # Extract timestamp and message
            bracket_end = content.index('] ')
            timestamp = content[1:bracket_end]  # Skip the opening bracket
            message = content[bracket_end + 2:]  # Skip '] '
            
            # Verify ISO timestamp format (YYYY-MM-DDTHH:MM:SS.ssssss)
            assert len(timestamp) >= 19, "Timestamp too short"
            assert timestamp[4] == '-', "Invalid year-month separator"
            assert timestamp[7] == '-', "Invalid month-day separator"
            assert timestamp[10] == 'T', "Invalid date-time separator"
            assert timestamp[13] == ':', "Invalid hour-minute separator"
            assert timestamp[16] == ':', "Invalid minute-second separator"
            
            # Verify message
            assert message == test_message, "Message content doesn't match"
            
        finally:
            # Restore original LOG_PATH
            mcpcat.modules.logging.LOG_PATH = original_log_path
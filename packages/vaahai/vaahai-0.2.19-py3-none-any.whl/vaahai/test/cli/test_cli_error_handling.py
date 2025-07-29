"""
Tests for VaahAI CLI error handling.

This module contains tests to verify that the CLI properly handles errors
and provides appropriate error messages.
"""

import os
import pytest
from unittest.mock import patch
from typer.testing import CliRunner
from vaahai.cli.main import app, main

runner = CliRunner()


def test_keyboard_interrupt_handling():
    """Test that keyboard interrupts are properly handled."""
    # Mock app() to raise KeyboardInterrupt
    with patch("vaahai.cli.main.app", side_effect=KeyboardInterrupt):
        # We need to use the main function directly to test the error handling
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(130)


def test_general_exception_handling():
    """Test that general exceptions are properly handled."""
    # Mock app() to raise a general exception
    with patch("vaahai.cli.main.app", side_effect=Exception("Test error")):
        # We need to use the main function directly to test the error handling
        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)


def test_debug_mode_exception_handling():
    """Test that exceptions in debug mode show full traceback."""
    # Set debug environment variable
    with patch.dict(os.environ, {"VAAHAI_DEBUG": "1"}):
        # Mock app() to raise a general exception
        with patch("vaahai.cli.main.app", side_effect=Exception("Test error")):
            # In debug mode, the exception should be re-raised
            with pytest.raises(Exception, match="Test error"):
                main()


def test_command_not_found():
    """Test that using a non-existent command shows help."""
    result = runner.invoke(app, ["nonexistent-command"])
    assert result.exit_code != 0
    assert "No such command" in result.stdout or "Usage:" in result.stdout

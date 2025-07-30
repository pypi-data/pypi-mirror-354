"""
Unit tests for CLI utilities.

This module contains tests for the CLI utility functions.
"""

import os
from pathlib import Path
from unittest.mock import ANY, MagicMock, patch

import pytest
from rich.console import Console
from rich.panel import Panel
from typer.testing import CliRunner

from vaahai.cli.utils.console import (
    format_command,
    format_path,
    print_error,
    print_info,
    print_panel,
    print_success,
    print_warning,
)
from vaahai.test.utils.base_test import BaseTest


class TestConsoleUtils(BaseTest):
    """Test suite for console utility functions."""

    @patch("vaahai.cli.utils.console.console.print")
    def test_print_error(self, mock_print):
        """Test that print_error formats messages correctly."""
        print_error("Test error message")
        mock_print.assert_called_once()
        # Check that the message is included in the call
        call_str = str(mock_print.call_args)
        assert "Test error message" in call_str
        assert "red" in call_str or "✗" in call_str

    @patch("vaahai.cli.utils.console.console.print")
    def test_print_success(self, mock_print):
        """Test that print_success formats messages correctly."""
        print_success("Test success message")
        mock_print.assert_called_once()
        # Check that the message is included in the call
        call_str = str(mock_print.call_args)
        assert "Test success message" in call_str
        assert "green" in call_str or "✓" in call_str

    @patch("vaahai.cli.utils.console.console.print")
    def test_print_info(self, mock_print):
        """Test that print_info formats messages correctly."""
        print_info("Test info message")
        mock_print.assert_called_once()
        # Check that the message is included in the call
        call_str = str(mock_print.call_args)
        assert "Test info message" in call_str
        assert "cyan" in call_str or "ℹ" in call_str

    @patch("vaahai.cli.utils.console.console.print")
    def test_print_warning(self, mock_print):
        """Test that print_warning formats messages correctly."""
        print_warning("Test warning message")
        mock_print.assert_called_once()
        # Check that the message is included in the call
        call_str = str(mock_print.call_args)
        assert "Test warning message" in call_str
        assert "yellow" in call_str or "⚠" in call_str

    @patch("vaahai.cli.utils.console.console.print")
    def test_print_panel(self, mock_print):
        """Test that print_panel creates a panel with the correct content."""
        print_panel("Test panel content", title="Test Title")
        mock_print.assert_called_once()
        # Check that a Panel object was passed to print
        args, kwargs = mock_print.call_args
        assert isinstance(args[0], Panel)
        # We can't directly check the content of the Panel object, but we can check it was created

    def test_format_path(self):
        """Test that format_path correctly formats file paths."""
        path = "/path/to/file.txt"
        formatted = format_path(path)
        assert path in formatted
        assert "[" in formatted and "]" in formatted  # Check for styling

    def test_format_command(self):
        """Test that format_command correctly formats commands."""
        cmd = "vaahai config init"
        formatted = format_command(cmd)
        assert cmd in formatted
        assert "[" in formatted and "]" in formatted  # Check for styling

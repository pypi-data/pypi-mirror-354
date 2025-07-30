"""
Unit tests for help utilities.

This module contains tests for the help utility functions.
"""

from unittest.mock import ANY, MagicMock, patch

import pytest
import typer

from vaahai.cli.utils.help import custom_callback, format_command_help, show_custom_help
from vaahai.test.utils.base_test import BaseTest


class TestHelpUtils(BaseTest):
    """Test suite for help utility functions."""

    @patch("vaahai.cli.utils.help.console.print")
    def test_format_command_help(self, mock_print):
        """Test that format_command_help formats help text correctly."""
        # Create a mock context
        mock_ctx = MagicMock()
        mock_ctx.command.help = "Test help text"
        mock_ctx.info_name = "test-command"
        mock_ctx.command.name = "test-command"
        mock_ctx.command.params = []
        mock_ctx.command.commands = {}

        # Call the function
        format_command_help(mock_ctx)

        # Verify console.print was called at least once
        assert mock_print.call_count > 0

    @patch("vaahai.cli.utils.help.console.print")
    def test_show_custom_help(self, mock_print):
        """Test that show_custom_help displays help correctly."""
        # Create a mock context
        mock_ctx = MagicMock()
        mock_ctx.command.name = "test-app"
        mock_ctx.command.help = "Test app help"
        mock_ctx.command.commands = {
            "cmd1": MagicMock(help="Command 1 help", name="cmd1"),
            "cmd2": MagicMock(help="Command 2 help", name="cmd2"),
        }

        # Call the function
        show_custom_help(mock_ctx)

        # Verify console.print was called at least once
        assert mock_print.call_count > 0

    def test_custom_callback(self):
        """Test that custom_callback calls show_custom_help when no subcommand is invoked."""
        # Create a mock context
        mock_ctx = MagicMock()
        mock_ctx.invoked_subcommand = None

        # Patch show_custom_help
        with patch("vaahai.cli.utils.help.show_custom_help") as mock_show_help:
            # Call the function
            custom_callback(mock_ctx)

            # Verify show_custom_help was called
            mock_show_help.assert_called_once_with(mock_ctx)

    def test_custom_callback_with_subcommand(self):
        """Test that custom_callback doesn't call show_custom_help when a subcommand is invoked."""
        # Create a mock context
        mock_ctx = MagicMock()
        mock_ctx.invoked_subcommand = "test-command"

        # Patch show_custom_help
        with patch("vaahai.cli.utils.help.show_custom_help") as mock_show_help:
            # Call the function
            custom_callback(mock_ctx)

            # Verify show_custom_help was not called
            mock_show_help.assert_not_called()

"""
Integration tests for config command.

This module contains tests for the config command and its interactions with the configuration system.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest
import toml
import typer

from vaahai.test.utils.base_test import BaseTest
from vaahai.test.utils.cli_helpers import assert_command_success


class TestConfigIntegration(BaseTest):
    """Test suite for config command integration."""

    def test_config_init_creates_directory(self):
        """Test that config init creates a config directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir)

            # Run config init with the temporary config path
            with patch.dict(os.environ, {"VAAHAI_CONFIG_DIR": str(config_path)}):
                init_result = self.invoke_cli(["config", "init"])
                assert_command_success(init_result)

            # Verify the config directory was created
            assert config_path.exists()
            assert config_path.is_dir()

            # Verify success message in output
            assert "Configuration initialized" in init_result.stdout

    @patch("vaahai.cli.commands.config.command.print_panel")
    @patch("pathlib.Path.exists")
    @patch("vaahai.cli.utils.config.load_config")
    def test_config_show(self, mock_load_config, mock_exists, mock_print_panel):
        """Test that config show displays configuration."""
        # Mock file existence check to return True
        mock_exists.return_value = True

        # Mock the config loading function to return a test config
        mock_config = {
            "llm": {"provider": "openai", "model": "gpt-4"},
            "agents": {"use_docker": False},
        }
        mock_load_config.return_value = mock_config

        # Run config show
        show_result = self.invoke_cli(["config", "show"])
        assert_command_success(show_result)

        # Verify that print_panel was called at least once
        assert mock_print_panel.call_count > 0

    @patch("pathlib.Path.mkdir")
    @patch("pathlib.Path.exists")
    @patch("vaahai.cli.commands.config.command.print_success")
    def test_config_init_with_custom_dir(
        self, mock_print_success, mock_exists, mock_mkdir
    ):
        """Test config init with a custom directory."""
        # Mock path.exists to return False so mkdir gets called
        mock_exists.return_value = False

        # Create a temporary directory path for testing
        custom_path = "/tmp/custom_vaahai_config"

        # Run config init with custom directory
        result = self.invoke_cli(["config", "init", "--dir", custom_path])
        assert_command_success(result)

        # Verify mkdir was called with the right parameters
        mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verify success message was printed
        mock_print_success.assert_called_once_with(
            "Configuration initialized successfully!"
        )

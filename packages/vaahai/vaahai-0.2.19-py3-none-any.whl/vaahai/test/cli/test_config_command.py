"""
Tests for VaahAI config command.

This module contains tests to verify that the config command and its subcommands
function correctly.
"""

import os
import tempfile
from pathlib import Path
import pytest
from unittest.mock import patch
from typer.testing import CliRunner
from vaahai.cli.main import app

runner = CliRunner()


def test_config_init_command():
    """Test that the config init command runs without errors."""
    result = runner.invoke(app, ["config", "init"])
    assert result.exit_code == 0
    assert "Configuration Wizard" in result.stdout
    assert "VaahAI Configuration Wizard" in result.stdout


def test_config_show_command():
    """Test that the config show command runs without errors."""
    # Create a temporary file to use as config
    with tempfile.NamedTemporaryFile(suffix='.toml') as temp_file:
        # Write some mock config content
        temp_file.write(b"[vaahai]\nname = 'test'\n")
        temp_file.flush()
        
        # Run the command with the temp file
        result = runner.invoke(app, ["config", "show", "--file", temp_file.name])
        assert result.exit_code == 0
        assert "Current Configuration" in result.stdout
        assert "VaahAI Configuration" in result.stdout


def test_config_show_command_file_not_found():
    """Test that the config show command handles missing files correctly."""
    # Use a non-existent file path
    result = runner.invoke(app, ["config", "show", "--file", "/path/to/nonexistent/config.toml"])
    assert result.exit_code == 1
    assert "Configuration file not found" in result.stdout

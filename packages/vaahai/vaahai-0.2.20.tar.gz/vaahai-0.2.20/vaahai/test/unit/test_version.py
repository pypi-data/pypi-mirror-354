"""
Unit tests for version functionality.

This module contains tests for the version command and version utilities.
"""

import importlib.metadata
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app
from vaahai.test.utils.base_test import BaseTest


class TestVersion(BaseTest):
    """Test suite for version functionality."""

    def test_version_command(self):
        """Test that the version command displays the correct version."""
        result = self.invoke_cli(["version", "show"])
        assert result.exit_code == 0
        assert "VaahAI version" in result.stdout

        # Get the actual version from metadata
        version = importlib.metadata.version("vaahai")
        assert version in result.stdout

    def test_version_flag(self):
        """Test that the --version flag displays the correct version."""
        result = self.invoke_cli(["--version"])
        assert result.exit_code == 0
        assert "VaahAI version" in result.stdout

        # Get the actual version from metadata
        version = importlib.metadata.version("vaahai")
        assert version in result.stdout

    @patch("importlib.metadata.version")
    def test_version_with_mock(self, mock_version):
        """Test version command with mocked version."""
        mock_version.return_value = "9.9.9"
        result = self.invoke_cli(["version", "show"])
        assert result.exit_code == 0
        assert "9.9.9" in result.stdout

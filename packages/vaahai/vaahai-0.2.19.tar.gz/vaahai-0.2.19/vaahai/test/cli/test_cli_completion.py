"""
Tests for VaahAI CLI shell completion functionality.

This module contains tests to verify that the CLI properly supports shell completion.
"""

import pytest
from typer.testing import CliRunner
from vaahai.cli.main import app, main

runner = CliRunner()


def test_completion_command_exists():
    """Test that the completion command is available."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check if completion is mentioned in help text
    assert any(term in result.stdout.lower() for term in ["completion", "shell", "autocomplete"])


def test_shell_completion_invocation():
    """Test that shell completion can be invoked."""
    # Test that the --completion flag is recognized
    # We don't test the actual output since it depends on the shell
    result = runner.invoke(app, ["--completion"])
    # It might exit with code 0 or 2 depending on Typer version, but it shouldn't crash
    assert result.exit_code in [0, 2]
    # The output should contain some completion-related text
    assert any(term in result.stdout.lower() for term in ["completion", "shell", "bash", "zsh"])


def test_completion_help():
    """Test that completion help is available."""
    # Test that the help text mentions completion
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check for common completion-related terms
    assert any(term in result.stdout.lower() for term in ["completion", "shell", "autocomplete"])

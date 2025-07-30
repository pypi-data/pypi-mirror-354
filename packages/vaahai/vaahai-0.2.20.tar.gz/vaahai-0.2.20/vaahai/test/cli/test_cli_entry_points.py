"""
Tests for VaahAI CLI entry points.

This module contains tests to verify that all CLI commands are properly registered
and accessible through the main entry point.
"""

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app, main

runner = CliRunner()


def test_main_help():
    """Test that the main CLI help command works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "vaahai" in result.stdout
    assert "Commands" in result.stdout
    # The options section might be called "Options" or "Global Options" depending on the formatting
    assert any(option in result.stdout for option in ["Options", "Global Options"])
    assert "--verbose" in result.stdout
    assert "--quiet" in result.stdout
    assert "--config" in result.stdout


def test_helloworld_command():
    """Test that the helloworld command is registered and accessible."""
    result = runner.invoke(app, ["helloworld", "--help"])
    assert result.exit_code == 0
    assert "helloworld" in result.stdout


def test_config_command():
    """Test that the config command is registered and accessible."""
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "config" in result.stdout
    # With custom help formatting, we're looking for the subcommands by name
    # rather than the exact "Commands" heading
    assert "init" in result.stdout
    assert "show" in result.stdout


def test_review_command():
    """Test that the review command is registered and accessible."""
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "review" in result.stdout


def test_audit_command():
    """Test that the audit command is registered and accessible."""
    result = runner.invoke(app, ["audit", "--help"])
    assert result.exit_code == 0
    assert "audit" in result.stdout


def test_version_command():
    """Test that the version command is registered and accessible."""
    result = runner.invoke(app, ["version", "--help"])
    assert result.exit_code == 0
    assert "version" in result.stdout


def test_global_verbose_option():
    """Test that the global verbose option is properly passed to commands."""
    result = runner.invoke(app, ["--verbose", "config", "init"])
    assert result.exit_code == 0
    assert "Configuration initialized successfully" in result.stdout


def test_global_quiet_option():
    """Test that the global quiet option suppresses non-essential output."""
    result = runner.invoke(app, ["--quiet", "config", "init"])
    assert result.exit_code == 0
    # In quiet mode, we should still see the success message but not the panel
    assert "Configuration initialized successfully" in result.stdout
    assert "Configuration Wizard" not in result.stdout


def test_conflicting_options():
    """Test that using both --verbose and --quiet options raises an error."""
    result = runner.invoke(app, ["--verbose", "--quiet", "config", "init"])
    assert result.exit_code == 1
    assert "Cannot use both --verbose and --quiet options together" in result.stdout


def test_invalid_config_file():
    """Test that specifying a non-existent config file raises an error."""
    result = runner.invoke(
        app, ["--config", "/path/to/nonexistent/config.toml", "config", "init"]
    )
    assert result.exit_code == 1
    assert "Config file not found" in result.stdout

"""
Tests for the VaahAI CLI command group structure.

This module contains tests for the command group structure of the VaahAI CLI,
including the core, project, and dev command groups.
"""

import pytest
from typer.testing import CliRunner
from vaahai.cli.main import app

runner = CliRunner()


def test_command_groups_exist():
    """Test that the command groups exist in the CLI."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check that all command groups are listed in the main help
    assert "core" in result.stdout
    assert "project" in result.stdout
    assert "dev" in result.stdout


def test_core_command_group():
    """Test that the core command group works."""
    result = runner.invoke(app, ["core", "--help"])
    assert result.exit_code == 0
    assert "Essential VaahAI commands" in result.stdout
    assert "config" in result.stdout
    assert "version" in result.stdout


def test_project_command_group():
    """Test that the project command group works."""
    result = runner.invoke(app, ["project", "--help"])
    assert result.exit_code == 0
    assert "Project analysis commands" in result.stdout
    assert "review" in result.stdout
    assert "audit" in result.stdout


def test_dev_command_group():
    """Test that the dev command group works."""
    result = runner.invoke(app, ["dev", "--help"])
    assert result.exit_code == 0
    assert "Development and testing commands" in result.stdout
    assert "helloworld" in result.stdout


def test_core_config_command():
    """Test that the core config command works."""
    result = runner.invoke(app, ["core", "config", "--help"])
    assert result.exit_code == 0
    # Check that the help text for the config command is displayed
    assert "Manage VaahAI configuration settings" in result.stdout


def test_project_review_command():
    """Test that the project review command works."""
    result = runner.invoke(app, ["project", "review", "--help"])
    assert result.exit_code == 0
    # Check that the help text for the review command is displayed
    assert "review" in result.stdout.lower()


def test_dev_helloworld_command():
    """Test that the dev helloworld command works."""
    result = runner.invoke(app, ["dev", "helloworld", "--help"])
    assert result.exit_code == 0
    # Check that the help text for the helloworld command is displayed
    assert "helloworld" in result.stdout.lower()


def test_backward_compatibility():
    """Test that the backward compatibility commands still work."""
    # Test direct access to config command
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "Manage VaahAI configuration settings" in result.stdout
    
    # Test direct access to review command
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "review" in result.stdout.lower()
    
    # Test direct access to helloworld command
    result = runner.invoke(app, ["helloworld", "--help"])
    assert result.exit_code == 0
    assert "helloworld" in result.stdout.lower()

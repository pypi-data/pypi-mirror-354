"""
Tests for custom help formatting in the VaahAI CLI.

This module contains tests to verify that the custom help formatting
is working correctly for all CLI commands and subcommands.
"""

import pytest
from typer.testing import CliRunner
from vaahai.cli.main import app
from vaahai.cli.utils.help import CustomHelpCommand, CustomHelpGroup, create_typer_app

runner = CliRunner()


def test_main_help_formatting():
    """Test that the main CLI help is formatted correctly."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check for Rich-formatted elements
    assert "Command Groups" in result.stdout
    assert "Commands (Direct Access)" in result.stdout
    assert "Global Options" in result.stdout
    assert "Environment Variables" in result.stdout
    assert "Quick Reference" in result.stdout


def test_command_group_help_formatting():
    """Test that command group help is formatted correctly."""
    # Test core command group
    result = runner.invoke(app, ["core", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout
    
    # Test project command group
    result = runner.invoke(app, ["project", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout
    
    # Test dev command group
    result = runner.invoke(app, ["dev", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout


def test_command_help_formatting():
    """Test that individual command help is formatted correctly."""
    # Test config command
    result = runner.invoke(app, ["config", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout
    
    # Test review command
    result = runner.invoke(app, ["review", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout
    
    # Test audit command
    result = runner.invoke(app, ["audit", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout
    
    # Test version command
    result = runner.invoke(app, ["version", "--help"])
    assert result.exit_code == 0
    assert "Subcommands" in result.stdout


def test_subcommand_help_formatting():
    """Test that subcommand help is formatted correctly."""
    # Test config init command
    result = runner.invoke(app, ["config", "init", "--help"])
    assert result.exit_code == 0
    assert "Options" in result.stdout
    
    # Test helloworld run command
    result = runner.invoke(app, ["helloworld", "run", "--help"])
    assert result.exit_code == 0
    
    # Test review run command
    result = runner.invoke(app, ["review", "run", "--help"])
    assert result.exit_code == 0
    assert "Options" in result.stdout


def test_create_typer_app():
    """Test that create_typer_app creates a Typer app with custom help formatting."""
    test_app = create_typer_app(
        name="test",
        help="Test app",
        add_completion=False,
    )
    assert test_app.info.name == "test"
    assert test_app.info.help == "Test app"
    # Verify that kwargs are passed correctly
    test_app_with_kwargs = create_typer_app(
        name="test",
        help="Test app",
        add_completion=False,
        context_settings={"help_option_names": ["--custom-help"]},
    )
    assert test_app_with_kwargs.info.name == "test"


def test_custom_help_command_class():
    """Test that CustomHelpCommand class exists and has required methods."""
    # Just verify the class has the expected methods
    assert hasattr(CustomHelpCommand, "get_help")
    assert hasattr(CustomHelpCommand, "list_commands")


def test_custom_help_group_class():
    """Test that CustomHelpGroup class exists and has required methods."""
    # Just verify the class has the expected methods
    assert hasattr(CustomHelpGroup, "get_help")
    assert hasattr(CustomHelpGroup, "list_commands")

"""
VaahAI config command implementation.

This module contains the implementation of the config command,
which is used to manage VaahAI configuration settings.
"""

import os
from pathlib import Path
import typer
from typing import Optional
from rich.console import Console

from vaahai.cli.utils.console import print_panel, print_success, print_info, print_error
from vaahai.cli.utils.help import create_typer_app, CustomHelpCommand

# Create a rich console for formatted output
console = Console()

# Create the config command group with custom help formatting
config_app = create_typer_app(
    name="config",
    help="Manage VaahAI configuration settings",
    add_completion=True,
    no_args_is_help=True,
)


@config_app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    Manage VaahAI configuration settings.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(show)


@config_app.command("init", cls=CustomHelpCommand)
def init(
    ctx: typer.Context,
    config_dir: Optional[Path] = typer.Option(
        None,
        "--dir",
        "-d",
        help="Custom configuration directory path",
    ),
):
    """
    Initialize VaahAI configuration with interactive prompts.
    
    This command guides you through setting up your VaahAI configuration,
    including LLM provider selection, API keys, model preferences, and Docker settings.
    """
    # Access global options
    verbose = ctx.parent.obj.get("verbose", False) if ctx.parent and ctx.parent.obj else False
    quiet = ctx.parent.obj.get("quiet", False) if ctx.parent and ctx.parent.obj else False
    
    # Determine config directory
    if not config_dir:
        config_dir = Path(os.environ.get("VAAHAI_CONFIG_DIR", Path.home() / ".vaahai"))
    
    if verbose:
        print_info(f"Using configuration directory: {config_dir}")
    
    # Only show the panel if not in quiet mode
    if not quiet:
        print_panel(
            "[bold blue]VaahAI Configuration Wizard[/bold blue]\n\n"
            "This is a placeholder for the configuration wizard.\n"
            "In the future, this will guide you through setting up:\n"
            "- LLM provider selection\n"
            "- API keys\n"
            "- Model preferences\n"
            "- Docker settings",
            title="Configuration Wizard",
            style="blue",
        )
    
    # Create config directory if it doesn't exist
    if not config_dir.exists():
        if verbose:
            print_info(f"Creating configuration directory: {config_dir}")
        config_dir.mkdir(parents=True, exist_ok=True)
    
    print_success("Configuration initialized successfully!")


@config_app.command("show", cls=CustomHelpCommand)
def show(
    ctx: typer.Context,
    config_file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Path to specific configuration file to display",
    ),
):
    """
    Display current VaahAI configuration settings.
    
    This command shows your current VaahAI configuration settings,
    including LLM provider, API keys (masked), model preferences, and Docker settings.
    """
    # Access global options
    verbose = ctx.parent.obj.get("verbose", False) if ctx.parent and ctx.parent.obj else False
    quiet = ctx.parent.obj.get("quiet", False) if ctx.parent and ctx.parent.obj else False
    
    # Determine config directory and file
    config_dir = Path(os.environ.get("VAAHAI_CONFIG_DIR", Path.home() / ".vaahai"))
    default_config_file = config_dir / "config.toml"
    
    if config_file:
        if not config_file.exists():
            print_error(f"Configuration file not found: {config_file}")
            raise typer.Exit(code=1)
    else:
        config_file = default_config_file
        if not config_file.exists():
            print_error(f"Default configuration file not found: {config_file}")
            print_info("Run 'vaahai config init' to create a configuration file")
            raise typer.Exit(code=1)
    
    if verbose:
        print_info(f"Reading configuration from: {config_file}")
    
    # Only show the panel if not in quiet mode
    if not quiet:
        print_panel(
            "[bold blue]VaahAI Configuration[/bold blue]\n\n"
            "This is a placeholder for displaying the configuration.\n"
            "In the future, this will show your current settings for:\n"
            "- LLM provider\n"
            "- API keys (masked)\n"
            "- Model preferences\n"
            "- Docker settings",
            title="Current Configuration",
            style="blue",
        )

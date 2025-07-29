"""
VaahAI helloworld command implementation.

This module contains the implementation of the helloworld command,
which is used to test the proper functioning of the VaahAI CLI.
"""

import typer
from vaahai.cli.utils.console import print_panel, print_success, console
from vaahai.cli.utils.help import create_typer_app, CustomHelpCommand

# Create the helloworld command group with custom help formatting
helloworld_app = create_typer_app(
    name="helloworld",
    help="Test command to verify proper functioning of VaahAI",
    add_completion=False,
)


@helloworld_app.callback()
def callback():
    """
    Test command to verify proper functioning of VaahAI.
    """
    pass


@helloworld_app.command("run", cls=CustomHelpCommand)
def run():
    """
    Run the helloworld command to test VaahAI functionality.
    """
    print_panel(
        "[bold green]Hello from VaahAI![/bold green]\n\n"
        "VaahAI CLI is working correctly.\n"
        "This is a placeholder for the actual helloworld command.",
        title="VaahAI Helloworld",
        style="green",
    )
    print_success("VaahAI CLI is ready to use!")

"""
VaahAI helloworld command implementation.

This module contains the implementation of the helloworld command,
which demonstrates the Hello World agent functionality using the new
autogen-agentchat and autogen-ext packages.
"""

import typer
from typing import Optional
import asyncio

from vaahai.cli.utils.console import console, print_panel, print_success, print_error
from vaahai.cli.utils.help import CustomHelpCommand, create_typer_app
from vaahai.agents.base.agent_factory import AgentFactory

# Create the helloworld command group with custom help formatting
helloworld_app = create_typer_app(
    name="helloworld",
    help="Demonstrate the Hello World agent functionality",
    add_completion=False,
    no_args_is_help=False,  # Don't show help when no args are provided
)


@helloworld_app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    test_mode: bool = typer.Option(
        False, "--test", "-t", help="Run in test mode without using the OpenAI API"
    ),
    temperature: float = typer.Option(
        0.7, "--temperature", "-T", help="Temperature for response generation"
    ),
):
    """
    Run the Hello World agent to demonstrate VaahAI agent functionality.
    
    This command creates and runs a Hello World agent that generates
    a friendly and humorous greeting using the AutoGen framework.
    """
    # Only run if called directly (not as a parent command)
    if ctx.invoked_subcommand is None:
        try:
            # Create the Hello World agent
            config = {
                "name": "HelloWorldAgent",
                "provider": "openai",
                "temperature": temperature,
                "_test_mode": test_mode
            }
            
            agent = AgentFactory.create_agent("hello_world", config)
            
            # Run the agent asynchronously
            try:
                # Try to get existing event loop
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # Create new event loop if one doesn't exist
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
            result = loop.run_until_complete(agent.run())
            
            if result.get("status") == "success":
                # Display the agent's response
                print_panel(
                    f"[bold blue]Response:[/bold blue] {result.get('response')}",
                    title="VaahAI Hello World Agent",
                    style="green",
                )
                print_success("Hello World agent response generated successfully!")
            else:
                # Display error message
                print_error(f"Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print_error(f"Failed to run Hello World agent: {str(e)}")

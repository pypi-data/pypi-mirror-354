"""
CLI testing helper utilities for VaahAI tests.

This module provides helper functions and classes for testing CLI commands.
"""

import contextlib
import io
import os
import sys
from typing import Dict, Generator, List, Optional, Tuple, Union

from typer.testing import CliRunner, Result

from vaahai.cli.main import app


def invoke_cli(
    args: List[str], env: Optional[Dict[str, str]] = None, catch_exceptions: bool = True
) -> Result:
    """
    Invoke the CLI with the given arguments and environment variables.

    Args:
        args: List of command line arguments
        env: Optional environment variables
        catch_exceptions: Whether to catch exceptions (default: True)

    Returns:
        Result object from the CLI invocation
    """
    runner = CliRunner()
    return runner.invoke(app, args, env=env, catch_exceptions=catch_exceptions)


def assert_command_success(
    result: Result, expected_output: Optional[str] = None
) -> None:
    """
    Assert that a command executed successfully and optionally check its output.

    Args:
        result: Result object from the CLI invocation
        expected_output: Optional string that should be present in the output
    """
    assert result.exit_code == 0, f"Command failed with output: {result.stdout}"
    if expected_output:
        assert (
            expected_output in result.stdout
        ), f"Expected output not found: {expected_output}"


def assert_command_failure(
    result: Result, expected_error: Optional[str] = None
) -> None:
    """
    Assert that a command failed and optionally check its error message.

    Args:
        result: Result object from the CLI invocation
        expected_error: Optional string that should be present in the error output
    """
    assert result.exit_code != 0, "Command succeeded but was expected to fail"
    if expected_error:
        assert (
            expected_error in result.stdout
        ), f"Expected error not found: {expected_error}"


@contextlib.contextmanager
def captured_output() -> Generator[Tuple[io.StringIO, io.StringIO], None, None]:
    """
    Context manager to capture stdout and stderr.

    Yields:
        Tuple of StringIO objects for stdout and stderr
    """
    new_out, new_err = io.StringIO(), io.StringIO()
    old_out, old_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield new_out, new_err
    finally:
        sys.stdout, sys.stderr = old_out, old_err


def create_test_config(
    config_path: str, config_data: Dict[str, Union[str, bool, int, Dict]]
) -> None:
    """
    Create a test configuration file with the given data.

    Args:
        config_path: Path to the configuration file
        config_data: Dictionary of configuration data
    """
    import toml

    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        toml.dump(config_data, f)

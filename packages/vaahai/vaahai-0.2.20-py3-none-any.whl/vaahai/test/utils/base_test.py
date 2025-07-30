"""
Base test class for VaahAI tests.

This module provides a base test class with common functionality for VaahAI tests.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
from typer.testing import CliRunner, Result

from vaahai.cli.main import app


class BaseTest:
    """Base test class for VaahAI tests."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up test class."""
        cls.runner = CliRunner()
        cls.test_data_dir = Path(__file__).parent.parent / "data"

    def invoke_cli(
        self,
        args: List[str],
        env: Optional[Dict[str, str]] = None,
        catch_exceptions: bool = True,
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
        return self.runner.invoke(app, args, env=env, catch_exceptions=catch_exceptions)

    def assert_command_success(
        self, result: Result, expected_output: Optional[str] = None
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
        self, result: Result, expected_error: Optional[str] = None
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

    @staticmethod
    def create_temp_file(content: str = "") -> str:
        """
        Create a temporary file with the given content.

        Args:
            content: Content to write to the file

        Returns:
            Path to the temporary file
        """
        with tempfile.NamedTemporaryFile(delete=False, mode="w") as tmp_file:
            tmp_file.write(content)
            return tmp_file.name

    @staticmethod
    def create_temp_dir() -> str:
        """
        Create a temporary directory.

        Returns:
            Path to the temporary directory
        """
        return tempfile.mkdtemp()

    @staticmethod
    def cleanup_temp_file(file_path: str) -> None:
        """
        Delete a temporary file.

        Args:
            file_path: Path to the file to delete
        """
        if os.path.exists(file_path):
            os.unlink(file_path)

    @staticmethod
    def cleanup_temp_dir(dir_path: str) -> None:
        """
        Delete a temporary directory.

        Args:
            dir_path: Path to the directory to delete
        """
        import shutil

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

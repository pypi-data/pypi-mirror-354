"""
Global pytest fixtures and configuration for VaahAI tests.

This module contains fixtures that are available to all test modules.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional

import pytest
from typer.testing import CliRunner

from vaahai.cli.main import app


@pytest.fixture
def cli_runner() -> CliRunner:
    """Return a Typer CLI runner for testing CLI commands."""
    return CliRunner()


@pytest.fixture
def invoke_cli():
    """Return a function to invoke the CLI with the given arguments."""
    runner = CliRunner()

    def _invoke(args: List[str], env: Optional[Dict[str, str]] = None) -> Any:
        """Invoke the CLI with the given arguments and environment variables."""
        return runner.invoke(app, args, env=env)

    return _invoke


@pytest.fixture
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir


@pytest.fixture
def temp_file() -> Generator[str, None, None]:
    """Create a temporary file for tests."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file_path = tmp_file.name
    try:
        yield tmp_file_path
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


@pytest.fixture
def test_data_dir() -> Path:
    """Return the path to the test data directory."""
    return Path(__file__).parent / "data"


@pytest.fixture
def mock_config_file(temp_file: str) -> str:
    """Create a mock configuration file for testing."""
    config_content = """
    [vaahai]
    verbose = false
    quiet = false

    [llm]
    provider = "openai"
    model = "gpt-4"

    [agents]
    default_agent = "assistant"
    """
    with open(temp_file, "w") as f:
        f.write(config_content)
    return temp_file

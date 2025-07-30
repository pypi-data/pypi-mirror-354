"""
Tests to verify that development tools are properly configured.
This is a simple test file to ensure that our code quality tools are working.
"""
import os
import subprocess
from pathlib import Path


def test_flake8_config_exists():
    """Test that the flake8 config file exists."""
    flake8_config = Path(".flake8")
    assert flake8_config.exists(), "Flake8 config file should exist"


def test_black_config_exists():
    """Test that the black config exists in pyproject.toml."""
    pyproject_toml = Path("pyproject.toml")
    assert pyproject_toml.exists(), "pyproject.toml file should exist"

    with open(pyproject_toml, "r") as f:
        content = f.read()

    assert (
        "[tool.black]" in content
    ), "Black configuration should exist in pyproject.toml"


def test_isort_config_exists():
    """Test that the isort config exists in pyproject.toml."""
    pyproject_toml = Path("pyproject.toml")
    assert pyproject_toml.exists(), "pyproject.toml file should exist"

    with open(pyproject_toml, "r") as f:
        content = f.read()

    assert (
        "[tool.isort]" in content
    ), "isort configuration should exist in pyproject.toml"

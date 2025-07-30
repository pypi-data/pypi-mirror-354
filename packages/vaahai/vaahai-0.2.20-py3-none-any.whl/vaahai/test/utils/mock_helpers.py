"""
Mock helper utilities for VaahAI tests.

This module provides mock objects and utilities for testing VaahAI components.
"""

import json
import os
from typing import Any, Dict, List, Optional, Union
from unittest.mock import MagicMock, patch

import pytest


class MockResponse:
    """Mock response object for testing HTTP requests."""

    def __init__(
        self,
        status_code: int = 200,
        json_data: Optional[Dict[str, Any]] = None,
        text: str = "",
        headers: Optional[Dict[str, str]] = None,
        raise_for_status: bool = False,
    ):
        """
        Initialize a mock response object.

        Args:
            status_code: HTTP status code
            json_data: Optional JSON data to return
            text: Optional text content
            headers: Optional response headers
            raise_for_status: Whether to raise an exception on status check
        """
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text
        self.content = text.encode("utf-8")
        self.headers = headers or {}
        self._raise_for_status = raise_for_status

    def json(self) -> Dict[str, Any]:
        """Return JSON data."""
        return self._json_data

    def raise_for_status(self) -> None:
        """Raise an exception if status code indicates an error."""
        if self._raise_for_status:
            from requests.exceptions import HTTPError

            raise HTTPError(f"Mock HTTP Error: {self.status_code}")


def mock_env_vars(env_vars: Dict[str, str]) -> Any:
    """
    Context manager to temporarily set environment variables for testing.

    Args:
        env_vars: Dictionary of environment variables to set

    Returns:
        Context manager that sets and restores environment variables
    """
    return patch.dict(os.environ, env_vars)


def create_mock_llm_response(
    content: str, model: str = "gpt-4", usage: Optional[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    Create a mock LLM response object.

    Args:
        content: Response content
        model: Model name
        usage: Optional token usage statistics

    Returns:
        Dictionary representing an LLM response
    """
    return {
        "id": "mock-response-id",
        "object": "chat.completion",
        "created": 1677858242,
        "model": model,
        "choices": [
            {
                "message": {"role": "assistant", "content": content},
                "index": 0,
                "finish_reason": "stop",
            }
        ],
        "usage": usage
        or {
            "prompt_tokens": 10,
            "completion_tokens": len(content) // 4,
            "total_tokens": len(content) // 4 + 10,
        },
    }


def mock_autogen_agent(
    name: str = "mock_agent", system_message: str = "I am a mock agent"
) -> MagicMock:
    """
    Create a mock Autogen agent for testing.

    Args:
        name: Agent name
        system_message: Agent system message

    Returns:
        MagicMock object representing an Autogen agent
    """
    mock_agent = MagicMock()
    mock_agent.name = name
    mock_agent.system_message = system_message
    mock_agent.send.return_value = {"content": "Mock response from agent"}
    mock_agent.initiate_chat.return_value = {"content": "Mock chat initiated"}
    return mock_agent

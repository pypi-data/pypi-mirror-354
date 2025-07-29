# VaahAI Tests Module

This directory contains the test suite for the VaahAI project.

## Test Structure

- Unit tests for individual components
- Integration tests for component interactions
- End-to-end tests for complete workflows
- Mock and fixture utilities for testing

## Test Organization

Tests are organized to mirror the package structure:

- `test_cli/` - Tests for CLI commands and utilities
- `test_agents/` - Tests for AI agent implementations
- `test_integration/` - Tests for component integration
- `test_e2e/` - End-to-end tests for complete workflows

## Running Tests

Tests are implemented using pytest and can be run with:

```bash
poetry run pytest
```

For specific test categories:

```bash
poetry run pytest vaahai/tests/test_cli
poetry run pytest vaahai/tests/test_agents
```

## Test Coverage

The project aims for high test coverage (at least 80%) to ensure robustness and reliability.

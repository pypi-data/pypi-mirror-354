# VaahAI Tests Module

This directory contains the comprehensive test suite for the VaahAI project.

## Test Structure

The test suite is organized into the following categories:

- **Unit Tests** (`/unit`): Tests for individual components in isolation
- **Integration Tests** (`/integration`): Tests for component interactions
- **CLI Tests** (`/cli`): Tests for CLI commands and interfaces
- **Test Utilities** (`/utils`): Helper functions and classes for testing
- **Test Data** (`/data`): Sample data and fixtures for tests

## Test Organization

Tests are organized to mirror the package structure:

- `unit/` - Unit tests for individual components
- `integration/` - Integration tests for component interactions
- `cli/` - Tests for CLI commands and interfaces
- `utils/` - Test utilities and helpers
  - `base_test.py` - Base test class with common functionality
  - `cli_helpers.py` - CLI testing helpers
  - `mock_helpers.py` - Mock objects and utilities

## Global Fixtures

Global fixtures are defined in `conftest.py` and include:

- `cli_runner` - Typer CLI runner for testing commands
- `invoke_cli` - Function to invoke CLI commands
- `temp_dir` - Temporary directory for tests
- `temp_file` - Temporary file for tests
- `test_data_dir` - Path to test data directory
- `mock_config_file` - Mock configuration file for testing

## Running Tests

Tests are implemented using pytest and can be run with:

```bash
poetry run pytest
```

For specific test categories:

```bash
poetry run pytest vaahai/test/unit
poetry run pytest vaahai/test/integration
poetry run pytest vaahai/test/cli
```

With coverage reporting:

```bash
poetry run pytest --cov=vaahai
```

## Test Coverage

The project aims for high test coverage (at least 80%) to ensure robustness and reliability.

## Adding New Tests

When adding new features, follow these steps:

1. Create unit tests for individual components
2. Create integration tests for component interactions
3. Create CLI tests for command-line functionality
4. Ensure all tests pass before submitting a pull request

For more detailed information on testing practices, see the [Testing Guide](/docs/development/testing.md).

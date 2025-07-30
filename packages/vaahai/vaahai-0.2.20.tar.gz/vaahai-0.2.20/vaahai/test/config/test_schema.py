"""
Tests for the configuration schema.
"""

import unittest
from vaahai.config.schema import (
    VaahAIConfig,
    validate_config,
    config_to_schema,
    schema_to_config
)
from vaahai.config.defaults import DEFAULT_CONFIG


class TestConfigSchema(unittest.TestCase):
    """Test cases for the configuration schema."""

    def test_validate_config_valid(self):
        """Test validating a valid configuration."""
        # Use the default configuration, which should be valid
        errors = validate_config(DEFAULT_CONFIG)
        self.assertEqual(len(errors), 0, f"Expected no errors, got: {errors}")

    def test_validate_config_invalid_provider(self):
        """Test validating a configuration with an invalid provider."""
        config = {
            "llm": {
                "provider": "invalid-provider"
            }
        }
        errors = validate_config(config)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Invalid LLM provider" in error for error in errors))

    def test_validate_config_invalid_output_format(self):
        """Test validating a configuration with an invalid output format."""
        config = {
            "output": {
                "format": "invalid-format"
            }
        }
        errors = validate_config(config)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Invalid output format" in error for error in errors))

    def test_validate_config_invalid_verbosity(self):
        """Test validating a configuration with an invalid verbosity level."""
        config = {
            "output": {
                "verbosity": "invalid-verbosity"
            }
        }
        errors = validate_config(config)
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Invalid verbosity level" in error for error in errors))

    def test_config_to_schema(self):
        """Test converting a configuration dictionary to a schema object."""
        # Convert the default configuration to a schema object
        schema = config_to_schema(DEFAULT_CONFIG)
        
        # Check that the schema object has the expected values
        self.assertEqual(schema.llm.provider, "openai")
        self.assertEqual(schema.llm.openai.model, "gpt-4")
        self.assertEqual(schema.llm.claude.model, "claude-3-sonnet-20240229")
        self.assertEqual(schema.docker.enabled, True)
        self.assertEqual(schema.docker.resource_limits.cpu, 2.0)
        self.assertEqual(schema.output.format, "terminal")
        self.assertEqual(schema.output.verbosity, "normal")
        self.assertEqual(schema.output.color, True)

    def test_schema_to_config(self):
        """Test converting a schema object to a configuration dictionary."""
        # Create a schema object
        schema = VaahAIConfig()
        schema.llm.provider = "claude"
        schema.llm.claude.model = "claude-3-opus"
        schema.docker.enabled = False
        
        # Convert the schema object to a configuration dictionary
        config = schema_to_config(schema)
        
        # Check that the configuration dictionary has the expected values
        self.assertEqual(config["llm"]["provider"], "claude")
        self.assertEqual(config["llm"]["claude"]["model"], "claude-3-opus")
        self.assertEqual(config["docker"]["enabled"], False)

    def test_roundtrip_conversion(self):
        """Test round-trip conversion between configuration dictionary and schema object."""
        # Start with the default configuration
        original_config = DEFAULT_CONFIG.copy()
        
        # Convert to schema object
        schema = config_to_schema(original_config)
        
        # Convert back to configuration dictionary
        converted_config = schema_to_config(schema)
        
        # Check that the key values are preserved
        self.assertEqual(converted_config["llm"]["provider"], original_config["llm"]["provider"])
        self.assertEqual(converted_config["llm"]["openai"]["model"], original_config["llm"]["openai"]["model"])
        self.assertEqual(converted_config["docker"]["enabled"], original_config["docker"]["enabled"])
        self.assertEqual(converted_config["output"]["format"], original_config["output"]["format"])


if __name__ == "__main__":
    unittest.main()

"""
Tests for the ConfigManager class.
"""

import os
import tempfile
import shutil
from pathlib import Path
import unittest
from unittest.mock import patch, MagicMock

from vaahai.config.manager import ConfigManager
from vaahai.config.defaults import DEFAULT_CONFIG
from vaahai.config.utils import get_user_config_dir, get_project_config_dir
from vaahai.config.loader import save_toml
from vaahai.config.schema import VaahAIConfig
from vaahai.config.llm_utils import list_providers, list_models


class TestConfigManager(unittest.TestCase):
    """Test cases for the ConfigManager class."""

    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.user_config_dir = self.temp_dir / "user" / ".vaahai"
        self.project_config_dir = self.temp_dir / "project" / ".vaahai"
        
        # Create directories
        self.user_config_dir.mkdir(parents=True, exist_ok=True)
        self.project_config_dir.mkdir(parents=True, exist_ok=True)
        
        # Save original environment variables
        self.original_env = os.environ.copy()
        
        # Clear any VAAHAI_ environment variables that might affect tests
        for key in list(os.environ.keys()):
            if key.startswith("VAAHAI_"):
                del os.environ[key]
        
        # Setup patches
        self.patches = [
            patch('vaahai.config.manager.get_user_config_dir', return_value=self.user_config_dir),
            patch('vaahai.config.manager.get_project_config_dir', return_value=self.project_config_dir),
            patch('vaahai.config.utils.get_user_config_dir', return_value=self.user_config_dir),
            patch('vaahai.config.utils.get_project_config_dir', return_value=self.project_config_dir),
        ]
        
        # Start all patches
        for p in self.patches:
            p.start()
    
    def tearDown(self):
        """Clean up the test environment."""
        # Restore original environment variables
        os.environ.clear()
        os.environ.update(self.original_env)
        
        # Stop all patches
        for p in self.patches:
            p.stop()
        
        # Remove temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_load_default_config(self):
        """Test loading default configuration."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Check that the default configuration is loaded
        self.assertEqual(config_manager.get("llm.provider"), "openai")
        self.assertEqual(config_manager.get("llm.openai.model"), "gpt-4")
        self.assertTrue(config_manager.get("docker.enabled"))
        self.assertEqual(config_manager.get("output.format"), "terminal")
    
    def test_save_and_load_config(self):
        """Test saving and loading configuration."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set some values
        config_manager.set("llm.provider", "claude")
        config_manager.set("llm.claude.model", "claude-3-opus")
        
        # Save the configuration
        self.assertTrue(config_manager.save(user_level=True))
        
        # Create a new ConfigManager instance to load the saved configuration
        new_config_manager = ConfigManager()
        
        # Check that the saved values are loaded
        self.assertEqual(new_config_manager.get("llm.provider"), "claude")
        self.assertEqual(new_config_manager.get("llm.claude.model"), "claude-3-opus")
    
    def test_merge_config(self):
        """Test merging configurations."""
        # Create user config
        user_config = {
            "llm": {
                "provider": "claude",
                "claude": {
                    "model": "claude-3-opus"
                }
            }
        }
        
        # Save user config
        user_config_path = self.user_config_dir / "config.toml"
        save_toml(user_config_path, user_config)
        
        # Create project config
        project_config = {
            "llm": {
                "provider": "junie",  # This should override user config
                "junie": {
                    "model": "junie-8b"
                }
            }
        }
        
        # Save project config
        project_config_path = self.project_config_dir / "config.toml"
        save_toml(project_config_path, project_config)
        
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Check that the project config overrides user config
        self.assertEqual(config_manager.get("llm.provider"), "junie")
        self.assertEqual(config_manager.get("llm.junie.model"), "junie-8b")
        self.assertEqual(config_manager.get("llm.claude.model"), "claude-3-opus")
    
    def test_env_var_overrides(self):
        """Test environment variable overrides."""
        # Set environment variables
        os.environ["VAAHAI_LLM_PROVIDER"] = "ollama"
        os.environ["VAAHAI_LLM_OLLAMA_MODEL"] = "llama3"
        
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Check that environment variables override config
        self.assertEqual(config_manager.get("llm.provider"), "ollama")
        self.assertEqual(config_manager.get("llm.ollama.model"), "llama3")
    
    def test_cli_overrides(self):
        """Test command-line overrides."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Apply CLI overrides
        config_manager.apply_cli_overrides({
            "llm.provider": "junie",
            "llm.junie.model": "junie-8b"
        })
        
        # Check that CLI overrides take precedence
        self.assertEqual(config_manager.get("llm.provider"), "junie")
        self.assertEqual(config_manager.get("llm.junie.model"), "junie-8b")
        
        # Set environment variables
        os.environ["VAAHAI_LLM_PROVIDER"] = "ollama"
        
        # Check that CLI overrides take precedence over environment variables
        self.assertEqual(config_manager.get("llm.provider"), "junie")
    
    def test_exists(self):
        """Test checking if configuration files exist."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Initially, no config files should exist
        self.assertFalse(config_manager.exists("user"))
        self.assertFalse(config_manager.exists("project"))
        
        # Create user config
        user_config_path = self.user_config_dir / "config.toml"
        save_toml(user_config_path, {})
        
        # Check that user config exists
        self.assertTrue(config_manager.exists("user"))
        self.assertFalse(config_manager.exists("project"))
        
        # Create project config
        project_config_path = self.project_config_dir / "config.toml"
        save_toml(project_config_path, {})
        
        # Check that both configs exist
        self.assertTrue(config_manager.exists("user"))
        self.assertTrue(config_manager.exists("project"))
    
    def test_reset(self):
        """Test resetting configuration to defaults."""
        # Create user config
        user_config = {
            "llm": {
                "provider": "claude"
            },
            "docker": {
                "enabled": False
            }
        }
        
        # Save user config
        user_config_path = self.user_config_dir / "config.toml"
        save_toml(user_config_path, user_config)
        
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Check that user config is loaded
        self.assertEqual(config_manager.get("llm.provider"), "claude")
        self.assertFalse(config_manager.get("docker.enabled"))
        
        # Reset configuration
        config_manager.reset()
        
        # Check that configuration is reset to defaults
        self.assertEqual(config_manager.get("llm.provider"), "openai")
        self.assertTrue(config_manager.get("docker.enabled"))
        
        # Set environment variables
        os.environ["VAAHAI_DOCKER_ENABLED"] = "false"
        
        # Check that environment variables still apply after reset
        self.assertEqual(config_manager.get("docker.enabled"), "false")
    
    def test_get_full_config(self):
        """Test getting the entire configuration."""
        # Create user config
        user_config = {
            "llm": {
                "provider": "claude"
            }
        }
        
        # Save user config
        user_config_path = self.user_config_dir / "config.toml"
        save_toml(user_config_path, user_config)
        
        # Set environment variables
        os.environ["VAAHAI_OUTPUT_FORMAT"] = "markdown"
        
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Apply CLI overrides
        config_manager.apply_cli_overrides({
            "docker.enabled": False
        })
        
        # Get the entire configuration
        config = config_manager.get_full_config()
        
        # Check that the configuration includes values from all sources
        self.assertEqual(config["llm"]["provider"], "claude")
        self.assertEqual(config["output"]["format"], "markdown")
        self.assertFalse(config["docker"]["enabled"])
    
    def test_get_schema(self):
        """Test getting configuration as a schema object."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set some values
        config_manager.set("llm.provider", "claude")
        config_manager.set("llm.claude.model", "claude-3-opus")
        config_manager.set("docker.enabled", False)
        
        # Get schema
        schema = config_manager.get_schema()
        
        # Check schema values
        self.assertIsInstance(schema, VaahAIConfig)
        self.assertEqual(schema.llm.provider, "claude")
        self.assertEqual(schema.llm.claude.model, "claude-3-opus")
        self.assertEqual(schema.docker.enabled, False)
    
    def test_validate(self):
        """Test configuration validation."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Default config should be valid
        errors = config_manager.validate()
        self.assertEqual(len(errors), 0)
        
        # Set an invalid provider
        config_manager.set("llm.provider", "invalid-provider")
        
        # Should have validation errors
        errors = config_manager.validate()
        self.assertGreater(len(errors), 0)
        self.assertTrue(any("Invalid LLM provider" in error for error in errors))
    
    def test_get_full_config_with_overrides(self):
        """Test getting the full configuration with all overrides applied."""
        # Create and save user config
        user_manager = ConfigManager()
        user_manager.set("llm.provider", "claude")
        user_manager.save(user_level=True)
        
        # Create and save project config
        project_manager = ConfigManager()
        project_manager.set("docker.enabled", False)
        project_manager.save(user_level=False)
        
        # Set environment variable
        os.environ["VAAHAI_OUTPUT_FORMAT"] = "json"
        
        # Create manager with CLI overrides
        manager = ConfigManager()
        manager.apply_cli_overrides({"llm.claude.model": "claude-3-opus"})
        
        # Get full config
        full_config = manager.get_full_config()
        
        # Check values with correct precedence
        self.assertEqual(full_config["llm"]["provider"], "claude")  # From user config
        self.assertEqual(full_config["llm"]["claude"]["model"], "claude-3-opus")  # From CLI
        self.assertEqual(full_config["docker"]["enabled"], False)  # From project config
        self.assertEqual(full_config["output"]["format"], "json")  # From env var
    
    # Tests for LLM provider-specific methods
    
    def test_get_current_provider(self):
        """Test getting the current LLM provider."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Default provider should be openai
        self.assertEqual(config_manager.get_current_provider(), "openai")
        
        # Set provider to claude
        config_manager.set("llm.provider", "claude")
        self.assertEqual(config_manager.get_current_provider(), "claude")
        
        # Set environment variable
        os.environ["VAAHAI_LLM_PROVIDER"] = "junie"
        self.assertEqual(config_manager.get_current_provider(), "junie")
        
        # CLI override should take precedence
        config_manager.apply_cli_overrides({"llm.provider": "ollama"})
        self.assertEqual(config_manager.get_current_provider(), "ollama")
    
    def test_set_provider(self):
        """Test setting the active LLM provider."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set valid provider
        config_manager.set_provider("claude")
        self.assertEqual(config_manager.get("llm.provider"), "claude")
        
        # Set another valid provider
        config_manager.set_provider("junie")
        self.assertEqual(config_manager.get("llm.provider"), "junie")
        
        # Try to set invalid provider
        with self.assertRaises(ValueError):
            config_manager.set_provider("invalid-provider")
    
    def test_get_provider_config(self):
        """Test getting configuration for a specific provider."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set some provider-specific configurations
        config_manager.set("llm.openai.model", "gpt-4")
        config_manager.set("llm.claude.model", "claude-3-opus")
        
        # Get OpenAI config
        openai_config = config_manager.get_provider_config("openai")
        self.assertIsInstance(openai_config, dict)
        self.assertEqual(openai_config.get("model"), "gpt-4")
        
        # Get Claude config
        claude_config = config_manager.get_provider_config("claude")
        self.assertIsInstance(claude_config, dict)
        self.assertEqual(claude_config.get("model"), "claude-3-opus")
        
        # Get current provider config (default is openai)
        current_config = config_manager.get_provider_config()
        self.assertEqual(current_config.get("model"), "gpt-4")
        
        # Set current provider to claude
        config_manager.set_provider("claude")
        current_config = config_manager.get_provider_config()
        self.assertEqual(current_config.get("model"), "claude-3-opus")
        
        # Try to get config for invalid provider
        with self.assertRaises(ValueError):
            config_manager.get_provider_config("invalid-provider")
    
    @patch('vaahai.config.llm_utils.validate_api_key', return_value=True)
    def test_set_api_key(self, mock_validate):
        """Test setting API key for a provider."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set API key for OpenAI
        config_manager.set_api_key("test-openai-key", "openai")
        self.assertEqual(config_manager.get("llm.openai.api_key"), "test-openai-key")
        
        # Set API key for current provider
        config_manager.set_provider("claude")
        config_manager.set_api_key("test-claude-key")
        self.assertEqual(config_manager.get("llm.claude.api_key"), "test-claude-key")
        
        # Try to set API key for invalid provider
        with self.assertRaises(ValueError):
            config_manager.set_api_key("test-key", "invalid-provider")
        
        # Try to set invalid API key
        mock_validate.return_value = False
        with self.assertRaises(ValueError):
            config_manager.set_api_key("", "openai")
    
    @patch.dict(os.environ, {
        "VAAHAI_OPENAI_API_KEY": "vaahai-openai-key",
        "OPENAI_API_KEY": "openai-key",
    })
    def test_get_api_key(self):
        """Test getting API key for a provider."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set API key in config
        config_manager.set("llm.claude.api_key", "config-claude-key")
        
        # Get API key from environment variable
        self.assertEqual(config_manager.get_api_key("openai"), "vaahai-openai-key")
        
        # Get API key from config
        self.assertEqual(config_manager.get_api_key("claude"), "config-claude-key")
        
        # Get API key for current provider
        self.assertEqual(config_manager.get_api_key(), "vaahai-openai-key")
        
        # Try to get API key for invalid provider
        with self.assertRaises(ValueError):
            config_manager.get_api_key("invalid-provider")
        
        # CLI override should take precedence
        config_manager.apply_cli_overrides({"llm.openai.api_key": "cli-openai-key"})
        # Clear environment variable cache to ensure CLI override is used
        config_manager._env_vars = {}  # Reset cached environment variables
        self.assertEqual(config_manager.get_api_key("openai"), "cli-openai-key")
    
    def test_get_model(self):
        """Test getting model for a provider."""
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Get default models
        self.assertEqual(config_manager.get_model("openai"), "gpt-4")
        self.assertEqual(config_manager.get_model("claude"), "claude-3-sonnet-20240229")
        
        # Set models in config
        config_manager.set("llm.openai.model", "gpt-3.5-turbo")
        config_manager.set("llm.claude.model", "claude-3-opus-20240229")
        
        # Get models from config
        self.assertEqual(config_manager.get_model("openai"), "gpt-3.5-turbo")
        self.assertEqual(config_manager.get_model("claude"), "claude-3-opus-20240229")
        
        # Get model for current provider
        self.assertEqual(config_manager.get_model(), "gpt-3.5-turbo")
        
        # Try to get model for invalid provider
        with self.assertRaises(ValueError):
            config_manager.get_model("invalid-provider")
    
    @patch('vaahai.config.manager.list_models')
    def test_set_model(self, mock_list_models):
        """Test setting model for a provider."""
        # Mock list_models to return valid models
        mock_list_models.side_effect = lambda provider: {
            "openai": ["gpt-4", "gpt-3.5-turbo"],
            "claude": ["claude-3-opus-20240229", "claude-3-sonnet-20240229"],
            "junie": ["junie-8b", "junie-20b"],
            "ollama": ["llama3", "llama2"],
        }[provider]
        
        # Create a new ConfigManager instance
        config_manager = ConfigManager()
        
        # Set valid models
        config_manager.set_model("gpt-3.5-turbo", "openai")
        self.assertEqual(config_manager.get("llm.openai.model"), "gpt-3.5-turbo")
        
        config_manager.set_provider("claude")
        config_manager.set_model("claude-3-opus-20240229")
        self.assertEqual(config_manager.get("llm.claude.model"), "claude-3-opus-20240229")
        
        # Try to set invalid model
        with self.assertRaises(ValueError):
            config_manager.set_model("invalid-model", "openai")
        
        # Try to set model for invalid provider
        with self.assertRaises(ValueError):
            config_manager.set_model("gpt-4", "invalid-provider")


if __name__ == "__main__":
    unittest.main()

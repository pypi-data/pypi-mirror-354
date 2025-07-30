"""
Tests for the configuration utility functions.
"""

import os
import tempfile
import shutil
from pathlib import Path
import unittest
from unittest.mock import patch

from vaahai.config.utils import (
    get_user_config_dir,
    get_project_config_dir,
    ensure_config_dir,
    get_env_var_name,
    get_env_var,
    set_nested_value,
    get_nested_value,
)


class TestConfigUtils(unittest.TestCase):
    """Test cases for the configuration utility functions."""

    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        
        # Save original environment variables
        self.original_env = os.environ.copy()
        
        # Set up environment variables for testing
        os.environ["VAAHAI_LLM_PROVIDER"] = "claude"
        os.environ["VAAHAI_DOCKER_ENABLED"] = "false"
    
    def tearDown(self):
        """Clean up the test environment."""
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
        
        # Restore original environment variables
        os.environ.clear()
        os.environ.update(self.original_env)
    
    def test_get_user_config_dir(self):
        """Test getting the user's configuration directory."""
        with patch('pathlib.Path.home', return_value=Path('/home/user')):
            user_config_dir = get_user_config_dir()
            self.assertEqual(user_config_dir, Path('/home/user/.vaahai'))
    
    def test_get_project_config_dir(self):
        """Test getting the project's configuration directory."""
        with patch('pathlib.Path.cwd', return_value=Path('/project')):
            project_config_dir = get_project_config_dir()
            self.assertEqual(project_config_dir, Path('/project/.vaahai'))
    
    def test_ensure_config_dir(self):
        """Test ensuring a configuration directory exists."""
        test_dir = self.temp_dir / "config"
        ensure_config_dir(test_dir)
        self.assertTrue(test_dir.exists())
        self.assertTrue(test_dir.is_dir())
    
    def test_get_env_var_name(self):
        """Test converting a configuration key to an environment variable name."""
        self.assertEqual(get_env_var_name("llm.provider"), "VAAHAI_LLM_PROVIDER")
        self.assertEqual(get_env_var_name("docker.enabled"), "VAAHAI_DOCKER_ENABLED")
    
    def test_get_env_var(self):
        """Test getting an environment variable for a configuration key."""
        self.assertEqual(get_env_var("llm.provider"), "claude")
        self.assertEqual(get_env_var("docker.enabled"), "false")
        self.assertIsNone(get_env_var("nonexistent.key"))
    
    def test_set_nested_value(self):
        """Test setting a nested value in a dictionary using dot notation."""
        config = {}
        
        # Set simple value
        set_nested_value(config, "key", "value")
        self.assertEqual(config["key"], "value")
        
        # Set nested value
        set_nested_value(config, "nested.key", "nested_value")
        self.assertEqual(config["nested"]["key"], "nested_value")
        
        # Set deeply nested value
        set_nested_value(config, "deeply.nested.key", "deeply_nested_value")
        self.assertEqual(config["deeply"]["nested"]["key"], "deeply_nested_value")
        
        # Override existing value
        set_nested_value(config, "key", "new_value")
        self.assertEqual(config["key"], "new_value")
        
        # Override existing nested value
        set_nested_value(config, "nested.key", "new_nested_value")
        self.assertEqual(config["nested"]["key"], "new_nested_value")
    
    def test_get_nested_value(self):
        """Test getting a nested value from a dictionary using dot notation."""
        config = {
            "key": "value",
            "nested": {
                "key": "nested_value"
            },
            "deeply": {
                "nested": {
                    "key": "deeply_nested_value"
                }
            }
        }
        
        # Get simple value
        self.assertEqual(get_nested_value(config, "key"), "value")
        
        # Get nested value
        self.assertEqual(get_nested_value(config, "nested.key"), "nested_value")
        
        # Get deeply nested value
        self.assertEqual(get_nested_value(config, "deeply.nested.key"), "deeply_nested_value")
        
        # Get nonexistent value
        self.assertIsNone(get_nested_value(config, "nonexistent.key"))
        
        # Get nonexistent value with default
        self.assertEqual(get_nested_value(config, "nonexistent.key", "default"), "default")


if __name__ == "__main__":
    unittest.main()

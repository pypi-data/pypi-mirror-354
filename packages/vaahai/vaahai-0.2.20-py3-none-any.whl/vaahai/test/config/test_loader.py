"""
Tests for the configuration file loading and saving utilities.
"""

import os
import tempfile
import shutil
from pathlib import Path
import unittest

from vaahai.config.loader import load_toml, save_toml


class TestConfigLoader(unittest.TestCase):
    """Test cases for the configuration file loading and saving utilities."""

    def setUp(self):
        """Set up the test environment."""
        # Create a temporary directory for testing
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up the test environment."""
        # Clean up temporary directory
        shutil.rmtree(self.temp_dir)
    
    def test_load_nonexistent_toml(self):
        """Test loading a nonexistent TOML file."""
        config = load_toml(self.temp_dir / "nonexistent.toml")
        self.assertEqual(config, {})
    
    def test_load_toml(self):
        """Test loading a TOML file."""
        # Create a test TOML file
        test_file = self.temp_dir / "test.toml"
        with open(test_file, "wb") as f:
            import tomli_w
            tomli_w.dump({"key": "value", "nested": {"key": "nested_value"}}, f)
        
        # Load the file
        config = load_toml(test_file)
        
        # Check the content
        self.assertEqual(config["key"], "value")
        self.assertEqual(config["nested"]["key"], "nested_value")
    
    def test_load_invalid_toml(self):
        """Test loading an invalid TOML file."""
        # Create an invalid TOML file
        test_file = self.temp_dir / "invalid.toml"
        with open(test_file, "w") as f:
            f.write("This is not valid TOML")
        
        # Load the file (should return empty dict on error)
        config = load_toml(test_file)
        self.assertEqual(config, {})
    
    def test_save_toml(self):
        """Test saving a TOML file."""
        # Define test data
        test_data = {
            "key": "value",
            "nested": {
                "key": "nested_value"
            },
            "list": [1, 2, 3],
            "bool": True
        }
        
        # Save the data
        test_file = self.temp_dir / "test.toml"
        result = save_toml(test_file, test_data)
        
        # Check the result
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Load the file and check the content
        with open(test_file, "rb") as f:
            import tomli
            loaded_data = tomli.load(f)
        
        self.assertEqual(loaded_data["key"], "value")
        self.assertEqual(loaded_data["nested"]["key"], "nested_value")
        self.assertEqual(loaded_data["list"], [1, 2, 3])
        self.assertEqual(loaded_data["bool"], True)
    
    def test_save_toml_create_dirs(self):
        """Test saving a TOML file with directory creation."""
        # Define test data
        test_data = {"key": "value"}
        
        # Save to a file in a nonexistent directory
        test_file = self.temp_dir / "subdir" / "test.toml"
        result = save_toml(test_file, test_data)
        
        # Check the result
        self.assertTrue(result)
        self.assertTrue(test_file.exists())
        
        # Load the file and check the content
        with open(test_file, "rb") as f:
            import tomli
            loaded_data = tomli.load(f)
        
        self.assertEqual(loaded_data["key"], "value")


if __name__ == "__main__":
    unittest.main()

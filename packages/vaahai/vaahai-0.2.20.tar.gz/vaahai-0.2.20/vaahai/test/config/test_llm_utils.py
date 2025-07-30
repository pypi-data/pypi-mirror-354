"""
Tests for LLM provider utilities.
"""

import os
import unittest
from unittest.mock import patch

from vaahai.config.llm_utils import (
    list_providers,
    list_models,
    get_default_model,
    validate_api_key,
    get_api_key_from_env,
    get_provider_config_path,
    PROVIDERS,
    OPENAI_MODELS,
    CLAUDE_MODELS,
    JUNIE_MODELS,
    OLLAMA_MODELS,
)


class TestLLMUtils(unittest.TestCase):
    """Test LLM provider utilities."""
    
    def test_list_providers(self):
        """Test listing providers."""
        providers = list_providers()
        self.assertEqual(providers, PROVIDERS)
        self.assertIn("openai", providers)
        self.assertIn("claude", providers)
        self.assertIn("junie", providers)
        self.assertIn("ollama", providers)
    
    def test_list_models(self):
        """Test listing models for providers."""
        # Test OpenAI models
        openai_models = list_models("openai")
        self.assertEqual(openai_models, OPENAI_MODELS)
        self.assertIn("gpt-4", openai_models)
        
        # Test Claude models
        claude_models = list_models("claude")
        self.assertEqual(claude_models, CLAUDE_MODELS)
        self.assertIn("claude-3-sonnet-20240229", claude_models)
        
        # Test Junie models
        junie_models = list_models("junie")
        self.assertEqual(junie_models, JUNIE_MODELS)
        self.assertIn("junie-8b", junie_models)
        
        # Test Ollama models
        ollama_models = list_models("ollama")
        self.assertEqual(ollama_models, OLLAMA_MODELS)
        self.assertIn("llama3", ollama_models)
        
        # Test invalid provider
        with self.assertRaises(ValueError):
            list_models("invalid_provider")
    
    def test_get_default_model(self):
        """Test getting default model for providers."""
        self.assertEqual(get_default_model("openai"), "gpt-4")
        self.assertEqual(get_default_model("claude"), "claude-3-sonnet-20240229")
        self.assertEqual(get_default_model("junie"), "junie-8b")
        self.assertEqual(get_default_model("ollama"), "llama3")
        
        # Test invalid provider
        with self.assertRaises(ValueError):
            get_default_model("invalid_provider")
    
    def test_validate_api_key(self):
        """Test validating API keys."""
        # Test valid API key
        self.assertTrue(validate_api_key("openai", "sk-1234567890"))
        self.assertTrue(validate_api_key("claude", "sk-ant-1234567890"))
        
        # Test empty API key
        self.assertFalse(validate_api_key("openai", ""))
        self.assertFalse(validate_api_key("claude", ""))
    
    @patch.dict(os.environ, {
        "VAAHAI_OPENAI_API_KEY": "vaahai-openai-key",
        "OPENAI_API_KEY": "openai-key",
        "VAAHAI_CLAUDE_API_KEY": "vaahai-claude-key",
    })
    def test_get_api_key_from_env(self):
        """Test getting API key from environment variables."""
        # Test VAAHAI_ prefixed variables take precedence
        self.assertEqual(get_api_key_from_env("openai"), "vaahai-openai-key")
        
        # Test fallback to non-prefixed variables
        with patch.dict(os.environ, {"VAAHAI_OPENAI_API_KEY": ""}):
            self.assertEqual(get_api_key_from_env("openai"), "openai-key")
        
        # Test VAAHAI_ prefixed variables for Claude
        self.assertEqual(get_api_key_from_env("claude"), "vaahai-claude-key")
        
        # Test missing environment variables
        self.assertIsNone(get_api_key_from_env("junie"))
    
    def test_get_provider_config_path(self):
        """Test getting provider configuration path."""
        self.assertEqual(get_provider_config_path("openai"), "llm.openai")
        self.assertEqual(get_provider_config_path("claude"), "llm.claude")
        self.assertEqual(get_provider_config_path("junie"), "llm.junie")
        self.assertEqual(get_provider_config_path("ollama"), "llm.ollama")
        
        # Test invalid provider
        with self.assertRaises(ValueError):
            get_provider_config_path("invalid_provider")


if __name__ == "__main__":
    unittest.main()

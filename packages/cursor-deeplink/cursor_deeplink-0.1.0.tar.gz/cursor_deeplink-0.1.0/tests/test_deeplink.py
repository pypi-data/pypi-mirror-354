"""
Unit tests for cursor_deeplink.deeplink module.
"""

import base64
import json
import unittest
import urllib.parse
from unittest.mock import patch

from cursor_deeplink.deeplink import DeeplinkGenerator, generate_deeplink


class TestDeeplinkGenerator(unittest.TestCase):
    """Test cases for DeeplinkGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = DeeplinkGenerator()
        self.sample_config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
        self.sample_name = "postgres"
    
    def test_generate_link_basic(self):
        """Test basic deeplink generation."""
        deeplink = self.generator.generate_link(self.sample_name, self.sample_config)
        
        # Check that it starts with the correct base URL
        self.assertTrue(deeplink.startswith(DeeplinkGenerator.BASE_URL))
        
        # Check that it contains the name parameter
        self.assertIn(f"name={self.sample_name}", deeplink)
        
        # Check that it contains a config parameter
        self.assertIn("config=", deeplink)
    
    def test_generate_link_config_encoding(self):
        """Test that the configuration is properly base64 encoded."""
        deeplink = self.generator.generate_link(self.sample_name, self.sample_config)
        
        # Parse the URL properly to extract config parameter
        parsed = urllib.parse.urlparse(deeplink)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        self.assertIn('config', query_params)
        encoded_config = query_params['config'][0]
        
        # Decode and verify
        decoded_json = base64.b64decode(encoded_config.encode('utf-8')).decode('utf-8')
        decoded_config = json.loads(decoded_json)
        
        self.assertEqual(decoded_config, self.sample_config)
    
    def test_generate_link_empty_name(self):
        """Test that empty name raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_link("", self.sample_config)
    
    def test_generate_link_none_name(self):
        """Test that None name raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_link(None, self.sample_config)
    
    def test_generate_link_invalid_config_type(self):
        """Test that non-dict config raises TypeError."""
        with self.assertRaises(TypeError):
            self.generator.generate_link(self.sample_name, "invalid config")
        
        with self.assertRaises(TypeError):
            self.generator.generate_link(self.sample_name, 123)
    
    def test_generate_from_mcp_config(self):
        """Test generating deeplink from MCP configuration."""
        mcp_config = {
            "postgres": self.sample_config,
            "sqlite": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/db.sqlite"]
            }
        }
        
        deeplink = self.generator.generate_from_mcp_config("postgres", mcp_config)
        
        # Should be the same as directly calling generate_link
        expected_deeplink = self.generator.generate_link("postgres", self.sample_config)
        self.assertEqual(deeplink, expected_deeplink)
    
    def test_generate_from_mcp_config_server_not_found(self):
        """Test that missing server in MCP config raises KeyError."""
        mcp_config = {
            "sqlite": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/db.sqlite"]
            }
        }
        
        with self.assertRaises(KeyError):
            self.generator.generate_from_mcp_config("postgres", mcp_config)
    
    def test_decode_config(self):
        """Test configuration decoding."""
        # Encode a config
        config_json = json.dumps(self.sample_config, separators=(',', ':'))
        encoded_config = base64.b64encode(config_json.encode('utf-8')).decode('utf-8')
        
        # Decode it back
        decoded_config = self.generator.decode_config(encoded_config)
        
        self.assertEqual(decoded_config, self.sample_config)
    
    def test_decode_config_invalid_base64(self):
        """Test that invalid base64 raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.decode_config("invalid base64!")
    
    def test_decode_config_invalid_json(self):
        """Test that invalid JSON raises ValueError."""
        # Encode invalid JSON
        invalid_json = "invalid json"
        encoded_invalid = base64.b64encode(invalid_json.encode('utf-8')).decode('utf-8')
        
        with self.assertRaises(ValueError):
            self.generator.decode_config(encoded_invalid)
    
    def test_parse_deeplink(self):
        """Test parsing a deeplink back to name and config."""
        deeplink = self.generator.generate_link(self.sample_name, self.sample_config)
        parsed = self.generator.parse_deeplink(deeplink)
        
        self.assertEqual(parsed['name'], self.sample_name)
        self.assertEqual(parsed['config'], self.sample_config)
    
    def test_parse_deeplink_invalid_url(self):
        """Test that invalid URL raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.parse_deeplink("https://example.com")
    
    def test_parse_deeplink_missing_params(self):
        """Test that missing parameters raise ValueError."""
        # URL with missing config parameter
        invalid_url = f"{DeeplinkGenerator.BASE_URL}?name=test"
        with self.assertRaises(ValueError):
            self.generator.parse_deeplink(invalid_url)
        
        # URL with missing name parameter
        invalid_url2 = f"{DeeplinkGenerator.BASE_URL}?config=dGVzdA=="
        with self.assertRaises(ValueError):
            self.generator.parse_deeplink(invalid_url2)
    
    def test_round_trip(self):
        """Test that generating and parsing a deeplink gives back the original data."""
        # Test with various configurations
        test_configs = [
            self.sample_config,
            {"command": "python", "args": ["-m", "server"]},
            {"command": "node", "args": ["server.js"], "env": {"PORT": "3000"}},
            {}  # Empty config
        ]
        
        for config in test_configs:
            with self.subTest(config=config):
                deeplink = self.generator.generate_link("test", config)
                parsed = self.generator.parse_deeplink(deeplink)
                
                self.assertEqual(parsed['name'], "test")
                self.assertEqual(parsed['config'], config)


class TestGenerateDeeplinkFunction(unittest.TestCase):
    """Test cases for the convenience function."""
    
    def test_generate_deeplink_function(self):
        """Test the convenience function works correctly."""
        config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
        
        deeplink = generate_deeplink("postgres", config)
        
        # Should be the same as using the class directly
        generator = DeeplinkGenerator()
        expected_deeplink = generator.generate_link("postgres", config)
        
        self.assertEqual(deeplink, expected_deeplink)


class TestSpecificExamples(unittest.TestCase):
    """Test cases for specific examples from the documentation."""
    
    def test_postgres_example(self):
        """Test the postgres example from the documentation."""
        config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
        
        generator = DeeplinkGenerator()
        deeplink = generator.generate_link("postgres", config)
        
        # Parse it back and verify
        parsed = generator.parse_deeplink(deeplink)
        self.assertEqual(parsed['name'], "postgres")
        self.assertEqual(parsed['config'], config)
        
        # Verify the structure
        self.assertTrue(deeplink.startswith("cursor://anysphere.cursor-deeplink/mcp/install"))
        self.assertIn("name=postgres", deeplink)
    
    def test_expected_base64_encoding(self):
        """Test that we generate the same base64 encoding as expected."""
        config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
        
        # The expected base64 from the documentation example
        expected_b64 = "eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBtb2RlbGNvbnRleHRwcm90b2NvbC9zZXJ2ZXItcG9zdGdyZXMiLCJwb3N0Z3Jlc3FsOi8vbG9jYWxob3N0L215ZGIiXX0="
        
        generator = DeeplinkGenerator()
        deeplink = generator.generate_link("postgres", config)
        
        # Parse the URL properly to extract config parameter
        parsed = urllib.parse.urlparse(deeplink)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        self.assertIn('config', query_params)
        actual_b64 = query_params['config'][0]
        
        # The base64 should match the expected one from the docs
        self.assertEqual(actual_b64, expected_b64)


class TestButtonGeneration(unittest.TestCase):
    """Test cases for button generation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = DeeplinkGenerator()
        self.sample_config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
        self.sample_name = "postgres"
    
    def test_generate_button_html_dark(self):
        """Test HTML button generation with dark theme."""
        html = self.generator.generate_button_html(self.sample_name, self.sample_config, theme="dark")
        
        self.assertIn('<a href="cursor://anysphere.cursor-deeplink/mcp/install', html)
        self.assertIn('background-color: #000', html)
        self.assertIn('color: #fff', html)
        self.assertIn('Add postgres MCP server to Cursor', html)
    
    def test_generate_button_html_light(self):
        """Test HTML button generation with light theme."""
        html = self.generator.generate_button_html(self.sample_name, self.sample_config, theme="light")
        
        self.assertIn('<a href="cursor://anysphere.cursor-deeplink/mcp/install', html)
        self.assertIn('background-color: #fff', html)
        self.assertIn('color: #000', html)
        self.assertIn('Add postgres MCP server to Cursor', html)
    
    def test_generate_button_html_custom_text(self):
        """Test HTML button generation with custom text."""
        custom_text = "Install PostgreSQL MCP Server"
        html = self.generator.generate_button_html(self.sample_name, self.sample_config, 
                                                  theme="dark", button_text=custom_text)
        
        self.assertIn(custom_text, html)
        self.assertNotIn('Add postgres MCP server to Cursor', html)
    
    def test_generate_button_html_invalid_theme(self):
        """Test that invalid theme raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_button_html(self.sample_name, self.sample_config, theme="invalid")
    
    def test_generate_button_jsx_dark(self):
        """Test JSX button generation with dark theme."""
        jsx = self.generator.generate_button_jsx(self.sample_name, self.sample_config, theme="dark")
        
        self.assertIn('<a href="cursor://anysphere.cursor-deeplink/mcp/install', jsx)
        self.assertIn("backgroundColor: '#000'", jsx)
        self.assertIn("color: '#fff'", jsx)
        self.assertIn('Add postgres MCP server to Cursor', jsx)
    
    def test_generate_button_jsx_light(self):
        """Test JSX button generation with light theme."""
        jsx = self.generator.generate_button_jsx(self.sample_name, self.sample_config, theme="light")
        
        self.assertIn('<a href="cursor://anysphere.cursor-deeplink/mcp/install', jsx)
        self.assertIn("backgroundColor: '#fff'", jsx)
        self.assertIn("color: '#000'", jsx)
        self.assertIn('Add postgres MCP server to Cursor', jsx)
    
    def test_generate_button_jsx_custom_text(self):
        """Test JSX button generation with custom text."""
        custom_text = "Install PostgreSQL MCP Server"
        jsx = self.generator.generate_button_jsx(self.sample_name, self.sample_config, 
                                                theme="dark", button_text=custom_text)
        
        self.assertIn(custom_text, jsx)
        self.assertNotIn('Add postgres MCP server to Cursor', jsx)
    
    def test_generate_button_jsx_invalid_theme(self):
        """Test that invalid theme raises ValueError."""
        with self.assertRaises(ValueError):
            self.generator.generate_button_jsx(self.sample_name, self.sample_config, theme="invalid")
    
    def test_generate_markdown_link(self):
        """Test Markdown link generation."""
        markdown = self.generator.generate_markdown_link(self.sample_name, self.sample_config)
        
        self.assertTrue(markdown.startswith('[Add postgres MCP server to Cursor]'))
        self.assertIn('(cursor://anysphere.cursor-deeplink/mcp/install', markdown)
        self.assertTrue(markdown.endswith(')'))
    
    def test_generate_markdown_link_custom_text(self):
        """Test Markdown link generation with custom text."""
        custom_text = "Install PostgreSQL MCP Server"
        markdown = self.generator.generate_markdown_link(self.sample_name, self.sample_config, 
                                                        button_text=custom_text)
        
        self.assertTrue(markdown.startswith(f'[{custom_text}]'))
        self.assertNotIn('Add postgres MCP server to Cursor', markdown)


if __name__ == '__main__':
    unittest.main() 
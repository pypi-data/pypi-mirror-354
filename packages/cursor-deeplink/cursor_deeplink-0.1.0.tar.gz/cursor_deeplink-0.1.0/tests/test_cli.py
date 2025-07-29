"""
Unit tests for cursor_deeplink.cli module.
"""

import json
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch, mock_open

from cursor_deeplink.cli import (
    create_parser, load_json_file, load_json_string,
    generate_command, generate_from_mcp_command, parse_command, main
)


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions in the CLI module."""
    
    def test_load_json_string_valid(self):
        """Test loading valid JSON string."""
        json_str = '{"command": "npx", "args": ["test"]}'
        result = load_json_string(json_str)
        expected = {"command": "npx", "args": ["test"]}
        self.assertEqual(result, expected)
    
    def test_load_json_string_invalid(self):
        """Test loading invalid JSON string exits with error."""
        with patch('sys.exit') as mock_exit:
            load_json_string('invalid json')
            mock_exit.assert_called_once_with(1)
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"test": "data"}')
    def test_load_json_file_valid(self, mock_file):
        """Test loading valid JSON file."""
        result = load_json_file('test.json')
        expected = {"test": "data"}
        self.assertEqual(result, expected)
        mock_file.assert_called_once_with('test.json', 'r', encoding='utf-8')
    
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_json_file_not_found(self, mock_file):
        """Test loading non-existent file exits with error."""
        with patch('sys.exit') as mock_exit:
            load_json_file('nonexistent.json')
            mock_exit.assert_called_once_with(1)
    
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    def test_load_json_file_invalid_json(self, mock_file):
        """Test loading file with invalid JSON exits with error."""
        with patch('sys.exit') as mock_exit:
            load_json_file('invalid.json')
            mock_exit.assert_called_once_with(1)


class TestParser(unittest.TestCase):
    """Test argument parser creation and functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = create_parser()
    
    def test_parser_no_args(self):
        """Test parser with no arguments."""
        # Should not raise an exception, but command will be None
        args = self.parser.parse_args([])
        self.assertIsNone(args.command)
    
    def test_generate_command_parsing(self):
        """Test parsing generate command."""
        args = self.parser.parse_args(['generate', 'postgres', '--config', '{"test": "data"}'])
        self.assertEqual(args.command, 'generate')
        self.assertEqual(args.name, 'postgres')
        self.assertEqual(args.config, '{"test": "data"}')
        self.assertIsNone(args.config_file)
    
    def test_generate_command_with_file(self):
        """Test parsing generate command with config file."""
        args = self.parser.parse_args(['generate', 'postgres', '--config-file', 'config.json'])
        self.assertEqual(args.command, 'generate')
        self.assertEqual(args.name, 'postgres')
        self.assertEqual(args.config_file, 'config.json')
        self.assertIsNone(args.config)
    
    def test_generate_from_mcp_command_parsing(self):
        """Test parsing generate-from-mcp command."""
        args = self.parser.parse_args(['generate-from-mcp', 'postgres', '--mcp-config', '{"test": "data"}'])
        self.assertEqual(args.command, 'generate-from-mcp')
        self.assertEqual(args.server_name, 'postgres')
        self.assertEqual(args.mcp_config, '{"test": "data"}')
        self.assertIsNone(args.mcp_file)
    
    def test_parse_command_parsing(self):
        """Test parsing parse command."""
        test_url = "cursor://anysphere.cursor-deeplink/mcp/install?name=test&config=dGVzdA=="
        args = self.parser.parse_args(['parse', test_url])
        self.assertEqual(args.command, 'parse')
        self.assertEqual(args.deeplink, test_url)
        self.assertEqual(args.output_format, 'text')  # default
    
    def test_parse_command_json_output(self):
        """Test parsing parse command with JSON output."""
        test_url = "cursor://anysphere.cursor-deeplink/mcp/install?name=test&config=dGVzdA=="
        args = self.parser.parse_args(['parse', test_url, '--output-format', 'json'])
        self.assertEqual(args.output_format, 'json')


class TestCommandFunctions(unittest.TestCase):
    """Test individual command functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
    
    @patch('cursor_deeplink.cli.load_json_string')
    @patch('builtins.print')
    def test_generate_command_with_config_string(self, mock_print, mock_load_json):
        """Test generate command with config string."""
        mock_load_json.return_value = self.sample_config
        
        # Mock argparse namespace
        class MockArgs:
            name = 'postgres'
            config = '{"test": "config"}'
            config_file = None
            format = 'url'
            theme = 'dark'
            button_text = None
        
        generate_command(MockArgs())
        
        mock_load_json.assert_called_once_with('{"test": "config"}')
        mock_print.assert_called_once()
        
        # Check that the printed value looks like a deeplink
        printed_value = mock_print.call_args[0][0]
        self.assertTrue(printed_value.startswith('cursor://anysphere.cursor-deeplink/mcp/install'))
    
    @patch('cursor_deeplink.cli.load_json_file')
    @patch('builtins.print')
    def test_generate_command_with_config_file(self, mock_print, mock_load_file):
        """Test generate command with config file."""
        mock_load_file.return_value = self.sample_config
        
        # Mock argparse namespace
        class MockArgs:
            name = 'postgres'
            config = None
            config_file = 'config.json'
            format = 'url'
            theme = 'dark'
            button_text = None
        
        generate_command(MockArgs())
        
        mock_load_file.assert_called_once_with('config.json')
        mock_print.assert_called_once()
    
    @patch('sys.exit')
    @patch('builtins.print')
    def test_generate_command_no_config(self, mock_print, mock_exit):
        """Test generate command with no config provided."""
        # Mock argparse namespace
        class MockArgs:
            name = 'postgres'
            config = None
            config_file = None
            format = 'url'
            theme = 'dark'
            button_text = None
        
        generate_command(MockArgs())
        
        # Should call sys.exit(1) when no config is provided
        mock_exit.assert_called_with(1)
    
    @patch('cursor_deeplink.cli.load_json_string')
    @patch('builtins.print')
    def test_generate_command_html_format(self, mock_print, mock_load_json):
        """Test generate command with HTML format."""
        mock_load_json.return_value = self.sample_config
        
        # Mock argparse namespace
        class MockArgs:
            name = 'postgres'
            config = '{"test": "config"}'
            config_file = None
            format = 'html'
            theme = 'dark'
            button_text = None
        
        generate_command(MockArgs())
        
        mock_load_json.assert_called_once_with('{"test": "config"}')
        mock_print.assert_called_once()
        
        # Check that the printed value looks like HTML
        printed_value = mock_print.call_args[0][0]
        self.assertTrue(printed_value.startswith('<a href="cursor://'))
        self.assertIn('background-color: #000', printed_value)
    
    @patch('cursor_deeplink.cli.load_json_string')
    @patch('builtins.print')
    def test_generate_command_jsx_format(self, mock_print, mock_load_json):
        """Test generate command with JSX format."""
        mock_load_json.return_value = self.sample_config
        
        # Mock argparse namespace
        class MockArgs:
            name = 'postgres'
            config = '{"test": "config"}'
            config_file = None
            format = 'jsx'
            theme = 'light'
            button_text = 'Custom Button Text'
        
        generate_command(MockArgs())
        
        mock_load_json.assert_called_once_with('{"test": "config"}')
        mock_print.assert_called_once()
        
        # Check that the printed value looks like JSX
        printed_value = mock_print.call_args[0][0]
        self.assertTrue(printed_value.startswith('<a href="cursor://'))
        self.assertIn("backgroundColor: '#fff'", printed_value)
        self.assertIn('Custom Button Text', printed_value)
    
    @patch('cursor_deeplink.cli.load_json_string')
    @patch('builtins.print')
    def test_generate_from_mcp_command(self, mock_print, mock_load_json):
        """Test generate-from-mcp command."""
        mcp_config = {"postgres": self.sample_config}
        mock_load_json.return_value = mcp_config
        
        # Mock argparse namespace
        class MockArgs:
            server_name = 'postgres'
            mcp_config = '{"postgres": {"test": "config"}}'
            mcp_file = None
            format = 'url'
            theme = 'dark'
            button_text = None
        
        generate_from_mcp_command(MockArgs())
        
        mock_load_json.assert_called_once_with('{"postgres": {"test": "config"}}')
        mock_print.assert_called_once()
    
    @patch('cursor_deeplink.deeplink.DeeplinkGenerator')
    @patch('builtins.print')
    def test_parse_command_text_output(self, mock_print, mock_generator_class):
        """Test parse command with text output."""
        mock_generator = mock_generator_class.return_value
        mock_generator.parse_deeplink.return_value = {
            'name': 'postgres',
            'config': self.sample_config
        }
        
        # Use a valid deeplink format
        test_deeplink = 'cursor://anysphere.cursor-deeplink/mcp/install?name=postgres&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBtb2RlbGNvbnRleHRwcm90b2NvbC9zZXJ2ZXItcG9zdGdyZXMiLCJwb3N0Z3Jlc3FsOi8vbG9jYWxob3N0L215ZGIiXX0='
        
        # Mock argparse namespace
        class MockArgs:
            deeplink = test_deeplink
            output_format = 'text'
        
        parse_command(MockArgs())
        
        # Should print name and config
        self.assertEqual(mock_print.call_count, 2)
        calls = mock_print.call_args_list
        self.assertTrue(calls[0][0][0].startswith('Name: postgres'))
        self.assertTrue(calls[1][0][0].startswith('Config: '))
    
    @patch('cursor_deeplink.deeplink.DeeplinkGenerator')
    @patch('builtins.print')
    def test_parse_command_json_output(self, mock_print, mock_generator_class):
        """Test parse command with JSON output."""
        mock_generator = mock_generator_class.return_value
        mock_generator.parse_deeplink.return_value = {
            'name': 'postgres',
            'config': self.sample_config
        }
        
        # Use a valid deeplink format
        test_deeplink = 'cursor://anysphere.cursor-deeplink/mcp/install?name=postgres&config=eyJjb21tYW5kIjoibnB4IiwiYXJncyI6WyIteSIsIkBtb2RlbGNvbnRleHRwcm90b2NvbC9zZXJ2ZXItcG9zdGdyZXMiLCJwb3N0Z3Jlc3FsOi8vbG9jYWxob3N0L215ZGIiXX0='
        
        # Mock argparse namespace
        class MockArgs:
            deeplink = test_deeplink
            output_format = 'json'
        
        parse_command(MockArgs())
        
        # Should print JSON
        mock_print.assert_called_once()
        printed_json = mock_print.call_args[0][0]
        parsed_json = json.loads(printed_json)
        self.assertEqual(parsed_json['name'], 'postgres')
        self.assertEqual(parsed_json['config'], self.sample_config)


class TestMainFunction(unittest.TestCase):
    """Test the main CLI entry point."""
    
    @patch('cursor_deeplink.cli.create_parser')
    def test_main_no_command(self, mock_create_parser):
        """Test main function with no command prints help and exits."""
        mock_parser = mock_create_parser.return_value
        mock_parser.parse_args.return_value.command = None
        
        with patch('sys.exit') as mock_exit:
            main()
            mock_parser.print_help.assert_called_once()
            mock_exit.assert_called_once_with(1)
    
    @patch('cursor_deeplink.cli.create_parser')
    def test_main_with_command(self, mock_create_parser):
        """Test main function with valid command calls function."""
        mock_parser = mock_create_parser.return_value
        mock_args = mock_parser.parse_args.return_value
        mock_args.command = 'generate'
        mock_func = unittest.mock.Mock()
        mock_args.func = mock_func
        
        main()
        
        mock_func.assert_called_once_with(mock_args)


class TestIntegration(unittest.TestCase):
    """Integration tests with real temporary files."""
    
    def test_real_config_file_integration(self):
        """Test with real temporary config file."""
        config = {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f)
            temp_file = f.name
        
        try:
            # Test loading the file
            loaded_config = load_json_file(temp_file)
            self.assertEqual(loaded_config, config)
        finally:
            import os
            os.unlink(temp_file)


if __name__ == '__main__':
    unittest.main() 
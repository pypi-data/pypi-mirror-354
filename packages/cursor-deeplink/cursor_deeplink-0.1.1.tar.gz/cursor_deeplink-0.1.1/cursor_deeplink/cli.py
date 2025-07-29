"""
Command-line interface for Cursor deeplink generation.
"""

import argparse
import json
import sys
from typing import Dict, Any

from .deeplink import DeeplinkGenerator


def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)


def load_json_string(json_str: str) -> Dict[str, Any]:
    """Load JSON from a string."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON string: {e}", file=sys.stderr)
        sys.exit(1)


def generate_command(args):
    """Handle the generate command."""
    generator = DeeplinkGenerator()
    
    # Load configuration from file or string
    config = None
    if args.config_file:
        config = load_json_file(args.config_file)
    elif args.config:
        config = load_json_string(args.config)
    else:
        print("Error: Either --config or --config-file must be provided.", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.format == 'url':
            result = generator.generate_link(args.name, config)
        elif args.format == 'html':
            result = generator.generate_button_html(args.name, config, args.theme, args.button_text)
        elif args.format == 'jsx':
            result = generator.generate_button_jsx(args.name, config, args.theme, args.button_text)
        elif args.format == 'markdown':
            result = generator.generate_markdown_link(args.name, config, args.button_text)
        else:
            result = generator.generate_link(args.name, config)
        
        print(result)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def generate_from_mcp_command(args):
    """Handle the generate-from-mcp command."""
    generator = DeeplinkGenerator()
    
    # Load MCP configuration
    if args.mcp_file:
        mcp_config = load_json_file(args.mcp_file)
    elif args.mcp_config:
        mcp_config = load_json_string(args.mcp_config)
    else:
        print("Error: Either --mcp-config or --mcp-file must be provided.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Extract the server config
        if args.server_name not in mcp_config:
            print(f"Error: Server '{args.server_name}' not found in MCP configuration", file=sys.stderr)
            sys.exit(1)
        
        config = mcp_config[args.server_name]
        
        if args.format == 'url':
            result = generator.generate_link(args.server_name, config)
        elif args.format == 'html':
            result = generator.generate_button_html(args.server_name, config, args.theme, args.button_text)
        elif args.format == 'jsx':
            result = generator.generate_button_jsx(args.server_name, config, args.theme, args.button_text)
        elif args.format == 'markdown':
            result = generator.generate_markdown_link(args.server_name, config, args.button_text)
        else:
            result = generator.generate_link(args.server_name, config)
        
        print(result)
    except (ValueError, TypeError, KeyError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def parse_command(args):
    """Handle the parse command."""
    generator = DeeplinkGenerator()
    
    try:
        parsed = generator.parse_deeplink(args.deeplink)
        if args.output_format == 'json':
            print(json.dumps(parsed, indent=2))
        else:
            print(f"Name: {parsed['name']}")
            print(f"Config: {json.dumps(parsed['config'], indent=2)}")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description='Generate Cursor deeplinks for MCP server installation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate deeplink URL (default)
  cursor-deeplink generate postgres --config '{"command": "npx", "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]}'
  
  # Generate dark HTML button
  cursor-deeplink generate postgres --config-file config.json --format html --theme dark
  
  # Generate light HTML button with custom text
  cursor-deeplink generate postgres --config-file config.json --format html --theme light --button-text "Install PostgreSQL MCP"
  
  # Generate JSX button component
  cursor-deeplink generate postgres --config-file config.json --format jsx --theme dark
  
  # Generate Markdown link
  cursor-deeplink generate postgres --config-file config.json --format markdown
  
  # Generate from MCP configuration file
  cursor-deeplink generate-from-mcp postgres --mcp-file mcp.json --format html --theme light
  
  # Parse an existing deeplink
  cursor-deeplink parse "cursor://anysphere.cursor-deeplink/mcp/install?name=postgres&config=..."
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a deeplink from server config')
    generate_parser.add_argument('name', help='Name of the MCP server')
    config_group = generate_parser.add_mutually_exclusive_group(required=True)
    config_group.add_argument('--config', help='JSON configuration string')
    config_group.add_argument('--config-file', help='Path to JSON configuration file')
    generate_parser.add_argument('--format', choices=['url', 'html', 'jsx', 'markdown'], 
                                default='url', help='Output format (default: url)')
    generate_parser.add_argument('--theme', choices=['dark', 'light'], default='dark',
                                help='Button theme for HTML/JSX formats (default: dark)')
    generate_parser.add_argument('--button-text', help='Custom button text (default: "Add {name} MCP server to Cursor")')
    generate_parser.set_defaults(func=generate_command)
    
    # Generate from MCP command
    mcp_parser = subparsers.add_parser('generate-from-mcp', help='Generate a deeplink from MCP configuration')
    mcp_parser.add_argument('server_name', help='Name of the server in the MCP configuration')
    mcp_config_group = mcp_parser.add_mutually_exclusive_group(required=True)
    mcp_config_group.add_argument('--mcp-config', help='JSON MCP configuration string')
    mcp_config_group.add_argument('--mcp-file', help='Path to MCP configuration file')
    mcp_parser.add_argument('--format', choices=['url', 'html', 'jsx', 'markdown'], 
                           default='url', help='Output format (default: url)')
    mcp_parser.add_argument('--theme', choices=['dark', 'light'], default='dark',
                           help='Button theme for HTML/JSX formats (default: dark)')
    mcp_parser.add_argument('--button-text', help='Custom button text (default: "Add {name} MCP server to Cursor")')
    mcp_parser.set_defaults(func=generate_from_mcp_command)
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse an existing deeplink')
    parse_parser.add_argument('deeplink', help='Cursor deeplink URL to parse')
    parse_parser.add_argument('--output-format', choices=['text', 'json'], default='text',
                             help='Output format (default: text)')
    parse_parser.set_defaults(func=parse_command)
    
    return parser


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main() 
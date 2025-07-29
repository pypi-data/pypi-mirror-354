"""
Core deeplink generation functionality for Cursor MCP server installation.
"""

import base64
import json
import urllib.parse
from typing import Dict, Any, Optional


class DeeplinkGenerator:
    """
    Generator for Cursor deeplinks for MCP server installation.
    
    Based on the format:
    cursor://anysphere.cursor-deeplink/mcp/install?name=$NAME&config=$BASE64_ENCODED_CONFIG
    """
    
    BASE_URL = "cursor://anysphere.cursor-deeplink/mcp/install"
    
    def __init__(self):
        """Initialize the DeeplinkGenerator."""
        pass
    
    def generate_link(self, name: str, config: Dict[str, Any]) -> str:
        """
        Generate a Cursor deeplink for MCP server installation.
        
        Args:
            name (str): The name of the MCP server
            config (Dict[str, Any]): The configuration dictionary for the server
            
        Returns:
            str: The generated deeplink URL
            
        Example:
            >>> generator = DeeplinkGenerator()
            >>> config = {
            ...     "command": "npx",
            ...     "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
            ... }
            >>> link = generator.generate_link("postgres", config)
        """
        if not name:
            raise ValueError("Server name cannot be empty")
        
        if not isinstance(config, dict):
            raise TypeError("Config must be a dictionary")
        
        # Convert config to JSON string and then base64 encode
        config_json = json.dumps(config, separators=(',', ':'))
        config_b64 = base64.b64encode(config_json.encode('utf-8')).decode('utf-8')
        
        # Build query parameters - manually construct to avoid encoding issues with base64
        name_encoded = urllib.parse.quote(name)
        deeplink = f"{self.BASE_URL}?name={name_encoded}&config={config_b64}"
        
        return deeplink
    
    def generate_from_mcp_config(self, server_name: str, mcp_config: Dict[str, Any]) -> str:
        """
        Generate a deeplink from an MCP configuration that contains the server config.
        
        Args:
            server_name (str): The name of the server to extract from the config
            mcp_config (Dict[str, Any]): The full MCP configuration containing server configs
            
        Returns:
            str: The generated deeplink URL
            
        Example:
            >>> generator = DeeplinkGenerator()
            >>> mcp_config = {
            ...     "postgres": {
            ...         "command": "npx",
            ...         "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
            ...     }
            ... }
            >>> link = generator.generate_from_mcp_config("postgres", mcp_config)
        """
        if server_name not in mcp_config:
            raise KeyError(f"Server '{server_name}' not found in MCP configuration")
        
        server_config = mcp_config[server_name]
        return self.generate_link(server_name, server_config)
    
    def decode_config(self, encoded_config: str) -> Dict[str, Any]:
        """
        Decode a base64 encoded configuration back to a dictionary.
        
        Args:
            encoded_config (str): Base64 encoded configuration string
            
        Returns:
            Dict[str, Any]: Decoded configuration dictionary
        """
        try:
            config_json = base64.b64decode(encoded_config.encode('utf-8')).decode('utf-8')
            return json.loads(config_json)
        except Exception as e:
            raise ValueError(f"Failed to decode configuration: {e}")
    
    def parse_deeplink(self, deeplink: str) -> Dict[str, Any]:
        """
        Parse a Cursor deeplink and extract the name and configuration.
        
        Args:
            deeplink (str): The Cursor deeplink URL
            
        Returns:
            Dict[str, Any]: Dictionary containing 'name' and 'config' keys
        """
        if not deeplink.startswith(self.BASE_URL):
            raise ValueError("Invalid Cursor deeplink format")
        
        # Parse the URL
        parsed = urllib.parse.urlparse(deeplink)
        query_params = urllib.parse.parse_qs(parsed.query)
        
        if 'name' not in query_params or 'config' not in query_params:
            raise ValueError("Deeplink missing required parameters")
        
        name = query_params['name'][0]
        encoded_config = query_params['config'][0]
        config = self.decode_config(encoded_config)
        
        return {
            'name': name,
            'config': config
        }
    
    def generate_button_html(self, name: str, config: Dict[str, Any], 
                           theme: str = "dark", button_text: Optional[str] = None) -> str:
        """
        Generate HTML button code for the deeplink.
        
        Args:
            name (str): The name of the MCP server
            config (Dict[str, Any]): The configuration dictionary for the server
            theme (str): Button theme, either "dark" or "light"
            button_text (str, optional): Custom button text, defaults to "Add {name} MCP server to Cursor"
            
        Returns:
            str: HTML button code
        """
        if theme not in ["dark", "light"]:
            raise ValueError("Theme must be either 'dark' or 'light'")
        
        deeplink = self.generate_link(name, config)
        if button_text is None:
            button_text = f"Add {name} MCP server to Cursor"
        
        # Define button styles based on theme
        if theme == "dark":
            button_style = (
                "background-color: #000; color: #fff; border: 1px solid #333; "
                "padding: 8px 16px; text-decoration: none; border-radius: 6px; "
                "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; "
                "font-size: 14px; font-weight: 500; display: inline-block; "
                "transition: background-color 0.2s ease;"
            )
            hover_style = (
                "onmouseover=\"this.style.backgroundColor='#333'\" "
                "onmouseout=\"this.style.backgroundColor='#000'\""
            )
        else:  # light theme
            button_style = (
                "background-color: #fff; color: #000; border: 1px solid #d0d7de; "
                "padding: 8px 16px; text-decoration: none; border-radius: 6px; "
                "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; "
                "font-size: 14px; font-weight: 500; display: inline-block; "
                "transition: background-color 0.2s ease;"
            )
            hover_style = (
                "onmouseover=\"this.style.backgroundColor='#f6f8fa'\" "
                "onmouseout=\"this.style.backgroundColor='#fff'\""
            )
        
        return f'<a href="{deeplink}" style="{button_style}" {hover_style}>{button_text}</a>'
    
    def generate_button_jsx(self, name: str, config: Dict[str, Any], 
                          theme: str = "dark", button_text: Optional[str] = None) -> str:
        """
        Generate JSX button component code for the deeplink.
        
        Args:
            name (str): The name of the MCP server
            config (Dict[str, Any]): The configuration dictionary for the server
            theme (str): Button theme, either "dark" or "light"
            button_text (str, optional): Custom button text, defaults to "Add {name} MCP server to Cursor"
            
        Returns:
            str: JSX button component code
        """
        if theme not in ["dark", "light"]:
            raise ValueError("Theme must be either 'dark' or 'light'")
        
        deeplink = self.generate_link(name, config)
        if button_text is None:
            button_text = f"Add {name} MCP server to Cursor"
        
        # Define button styles based on theme
        if theme == "dark":
            style_object = """{
    backgroundColor: '#000',
    color: '#fff',
    border: '1px solid #333',
    padding: '8px 16px',
    textDecoration: 'none',
    borderRadius: '6px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontSize: '14px',
    fontWeight: '500',
    display: 'inline-block',
    transition: 'background-color 0.2s ease',
    ':hover': {
      backgroundColor: '#333'
    }
  }"""
        else:  # light theme
            style_object = """{
    backgroundColor: '#fff',
    color: '#000',
    border: '1px solid #d0d7de',
    padding: '8px 16px',
    textDecoration: 'none',
    borderRadius: '6px',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    fontSize: '14px',
    fontWeight: '500',
    display: 'inline-block',
    transition: 'background-color 0.2s ease',
    ':hover': {
      backgroundColor: '#f6f8fa'
    }
  }"""
        
        return f"""<a href="{deeplink}" style={style_object}>
  {button_text}
</a>"""
    
    def generate_markdown_link(self, name: str, config: Dict[str, Any], 
                             button_text: Optional[str] = None) -> str:
        """
        Generate Markdown link for the deeplink.
        
        Args:
            name (str): The name of the MCP server
            config (Dict[str, Any]): The configuration dictionary for the server
            button_text (str, optional): Custom link text, defaults to "Add {name} MCP server to Cursor"
            
        Returns:
            str: Markdown link
        """
        deeplink = self.generate_link(name, config)
        if button_text is None:
            button_text = f"Add {name} MCP server to Cursor"
        
        return f"[{button_text}]({deeplink})"


def generate_deeplink(name: str, config: Dict[str, Any]) -> str:
    """
    Convenience function to generate a Cursor deeplink.
    
    Args:
        name (str): The name of the MCP server
        config (Dict[str, Any]): The configuration dictionary for the server
        
    Returns:
        str: The generated deeplink URL
    """
    generator = DeeplinkGenerator()
    return generator.generate_link(name, config) 
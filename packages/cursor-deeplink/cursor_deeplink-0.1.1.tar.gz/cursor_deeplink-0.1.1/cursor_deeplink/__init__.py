"""
Cursor Deeplink Generator

A Python package for generating Cursor deeplinks for MCP server installation.
"""

__version__ = "0.1.1"
__author__ = "Cursor Deeplink Generator"

from .deeplink import DeeplinkGenerator, generate_deeplink

__all__ = ["DeeplinkGenerator", "generate_deeplink"] 
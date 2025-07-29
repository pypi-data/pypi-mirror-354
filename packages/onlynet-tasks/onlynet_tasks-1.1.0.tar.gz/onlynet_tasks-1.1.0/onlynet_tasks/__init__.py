"""
OnlyNet Tasks MCP Server

A Model Context Protocol (MCP) server for generating Product Requirements Documents (PRDs)
and creating task breakdowns with complexity levels for software development projects.

Designed specifically for integration with Cursor agents and similar development tools.
"""

__version__ = "1.0.0"
__author__ = "OnlyNet"

from .server import main

__all__ = ["main"]

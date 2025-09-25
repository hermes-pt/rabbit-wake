#!/usr/bin/env python3
"""
Wake E-commerce Users MCP Server
MCP server for user-related operations in Wake e-commerce API
"""

from fastmcp import FastMCP
from wake.api import wake_client

# Initialize MCP server for users
mcp = FastMCP("Wake Users API")


if __name__ == "__main__":
    print("Starting Wake Users MCP Server...")
    mcp.run()
#!/usr/bin/env python3
"""
Wake MCP Server

Main MCP server that aggregates Wake e-commerce services.
"""

from fastmcp import FastMCP

# Import the products server
from src.wake.servers.products_server import mcp as products_server
# Import the simple login server
from src.wake.servers.simple_login_server import mcp as simple_login_server
# Import the checkout server
from src.wake.servers.checkout_server import mcp as checkout_server


# Create main MCP server
mcp = FastMCP("Camys")

# Mount the products server with empty prefix to keep original names
mcp.mount("products", products_server)
# Mount the simple login server
mcp.mount("auth", simple_login_server)
# Mount the checkout server
mcp.mount("checkout", checkout_server)


if __name__ == "__main__":
    mcp.run()
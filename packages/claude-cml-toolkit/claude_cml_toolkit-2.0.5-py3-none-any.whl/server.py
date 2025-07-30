"""
CML MCP Server - Main Entry Point

A modular toolkit for interacting with Cisco Modeling Labs (CML) through the
Model Context Protocol (MCP) interface.

Authors: Claude AI Assistant
Version: 2.0.0
License: MIT
"""

import os
import sys
from fastmcp import FastMCP

# Import all handler registration functions
from handlers import (
    register_lab_management_tools,
    register_topology_tools,
    register_configuration_tools,
    register_console_tools
)

# Create the MCP server
mcp = FastMCP(
    "CML Lab Builder",
    dependencies=["httpx>=0.26.0", "urllib3>=2.0.0"],
)

def register_all_tools():
    """Register all CML tools with the MCP server"""
    print("Registering CML MCP tools...", file=sys.stderr)
    
    # Register all tool groups
    register_lab_management_tools(mcp)
    register_topology_tools(mcp)
    register_configuration_tools(mcp)
    register_console_tools(mcp)
    
    print("All CML MCP tools registered successfully", file=sys.stderr)


# Register all tools when the module is imported
register_all_tools()


def main():
    """Main entry point for the CML MCP server"""
    print("Starting CML MCP Server...", file=sys.stderr)
    mcp.run()


# Main entry point
if __name__ == "__main__":
    main()

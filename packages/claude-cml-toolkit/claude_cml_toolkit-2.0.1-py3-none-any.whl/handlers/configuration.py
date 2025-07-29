"""
Configuration Handler

Handles device configuration management in CML labs.
"""

from typing import Dict, Any
from fastmcp import FastMCP

from ..client import get_client
from ..utils import check_auth


def register_configuration_tools(mcp: FastMCP):
    """Register configuration management tools with the MCP server"""
    
    @mcp.tool()
    async def configure_node(lab_id: str, node_id: str, config: str) -> str:
        """
        Configure a node with the specified configuration
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node to configure
            config: Configuration text to apply
        
        Returns:
            Confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request(
                "PUT",
                f"/api/v0/labs/{lab_id}/nodes/{node_id}/config",
                content=config
            )
            
            return f"Configuration applied to node {node_id}"
        except Exception as e:
            return f"Error configuring node: {str(e)}"

    @mcp.tool()
    async def get_node_config(lab_id: str, node_id: str) -> str:
        """
        Get the current configuration of a node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
        
        Returns:
            Node configuration text or error message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes/{node_id}/config")
            config = response.text
            return config
        except Exception as e:
            return f"Error getting node configuration: {str(e)}"

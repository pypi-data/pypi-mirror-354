"""
Lab Management Handler

Handles creation, deletion, listing, and control of CML labs.
"""

import sys
import asyncio
from typing import Dict, Any, Union
from fastmcp import FastMCP

from client import get_client, set_client, CMLAuth
from utils import check_auth, handle_api_error


# Actual function implementations (not wrapped as tools)
async def _get_lab_details(lab_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific lab
    
    Args:
        lab_id: ID of the lab to get details for
    
    Returns:
        Dictionary containing lab details
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check
    
    try:
        response = await get_client().request("GET", f"/api/v0/labs/{lab_id}")
        lab_details = response.json()
        return lab_details
    except Exception as e:
        return handle_api_error("get_lab_details", e)


async def _stop_lab(lab_id: str) -> str:
    """
    Stop the specified lab
    
    Args:
        lab_id: ID of the lab to stop
    
    Returns:
        Confirmation message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        response = await get_client().request("PUT", f"/api/v0/labs/{lab_id}/stop")
        return f"Lab {lab_id} stopped successfully"
    except Exception as e:
        return f"Error stopping lab: {str(e)}"


async def _start_lab(lab_id: str) -> str:
    """
    Start the specified lab
    
    Args:
        lab_id: ID of the lab to start
    
    Returns:
        Confirmation message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        response = await get_client().request("PUT", f"/api/v0/labs/{lab_id}/start")
        return f"Lab {lab_id} started successfully"
    except Exception as e:
        return f"Error starting lab: {str(e)}"


async def _get_lab_nodes(lab_id: str) -> Union[Dict[str, Any], str]:
    """
    Get all nodes in a specific lab (duplicate from topology for internal use)
    
    Args:
        lab_id: ID of the lab
    
    Returns:
        Dictionary of nodes in the lab or error message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        # First get the list of node IDs
        response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes")
        node_ids = response.json()
        
        print(f"Got node IDs: {node_ids}", file=sys.stderr)
        
        # If we get a list of IDs, fetch details for each node
        if isinstance(node_ids, list):
            result = {}
            for node_id in node_ids:
                try:
                    # Get detailed information for each node
                    node_response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes/{node_id}")
                    node_data = node_response.json()
                    result[node_id] = node_data
                except Exception as e:
                    print(f"Error getting details for node {node_id}: {str(e)}", file=sys.stderr)
                    # Add minimal info if detail fetch fails
                    result[node_id] = {"id": node_id, "label": f"Node-{node_id[:8]}"}
            
            return result
        else:
            # If it's already a dictionary, return as-is
            return node_ids
            
    except Exception as e:
        return f"Error getting lab nodes: {str(e)}"


def register_lab_management_tools(mcp: FastMCP):
    """Register lab management tools with the MCP server"""
    
    @mcp.tool()
    async def initialize_client(base_url: str, username: str, password: str, verify_ssl: bool = True) -> str:
        """
        Initialize the CML client with authentication credentials
        
        Args:
            base_url: Base URL of the CML server (e.g., https://cml-server)
            username: Username for CML authentication
            password: Password for CML authentication
            verify_ssl: Whether to verify SSL certificates (set to False for self-signed certificates)
        
        Returns:
            A success message if authentication is successful
        """
        # Fix URL if it doesn't have a scheme
        if not base_url.startswith(('http://', 'https://')):
            base_url = f"https://{base_url}"
        
        print(f"Initializing CML client with base_url: {base_url}", file=sys.stderr)
        cml_auth = CMLAuth(base_url, username, password, verify_ssl)
        
        try:
            token = await cml_auth.authenticate()
            print(f"Token received: {token[:10]}...", file=sys.stderr)  # Only print first 10 chars for security
            set_client(cml_auth)
            ssl_status = "enabled" if verify_ssl else "disabled (accepting self-signed certificates)"
            return f"Successfully authenticated with CML at {base_url} (SSL verification: {ssl_status})"
        except Exception as e:
            print(f"Error connecting to CML: {str(e)}", file=sys.stderr)
            return f"Error connecting to CML: {str(e)}"

    @mcp.tool()
    async def list_labs() -> str:
        """
        List all labs in CML
        
        Returns:
            A formatted list of all available labs
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            print("Attempting to list labs...", file=sys.stderr)
            response = await get_client().request("GET", "/api/v0/labs")
            labs = response.json()
            
            print(f"Found {len(labs)} labs", file=sys.stderr)
            
            if not labs:
                return "No labs found in CML."
            
            # Format the response nicely
            result = "Available Labs:\n\n"
            for lab_id, lab_info in labs.items():
                result += f"- {lab_info.get('title', 'Untitled')} (ID: {lab_id})\n"
                if lab_info.get('description'):
                    result += f"  Description: {lab_info['description']}\n"
                result += f"  State: {lab_info.get('state', 'unknown')}\n"
            
            return result
        except Exception as e:
            return f"Error listing labs: {str(e)}"

    @mcp.tool()
    async def create_lab(title: str, description: str = "") -> Dict[str, str]:
        """
        Create a new lab in CML
        
        Args:
            title: Title of the new lab
            description: Optional description for the lab
        
        Returns:
            Dictionary containing lab ID and confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            print(f"Creating lab with title: {title}", file=sys.stderr)
            
            response = await get_client().request(
                "POST", 
                "/api/v0/labs",
                json={"title": title, "description": description}
            )
            
            lab_data = response.json()
            print(f"Lab creation response: {lab_data}", file=sys.stderr)
            
            lab_id = lab_data.get("id")
            
            if not lab_id:
                return {"error": "Failed to create lab, no lab ID returned"}
            
            return {
                "lab_id": lab_id,
                "message": f"Created lab '{title}' with ID: {lab_id}",
                "status": "success"
            }
        except Exception as e:
            return handle_api_error("create_lab", e)

    @mcp.tool()
    async def get_lab_details(lab_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific lab
        
        Args:
            lab_id: ID of the lab to get details for
        
        Returns:
            Dictionary containing lab details
        """
        return await _get_lab_details(lab_id)

    @mcp.tool()
    async def delete_lab(lab_id: str) -> str:
        """
        Delete a lab from CML
        
        Args:
            lab_id: ID of the lab to delete
        
        Returns:
            Confirmation message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            # First check if the lab is running
            lab_details = await _get_lab_details(lab_id)
            if isinstance(lab_details, dict) and lab_details.get("state") == "STARTED":
                # Stop the lab first
                await _stop_lab(lab_id)
                # Wait for the lab to fully stop
                await asyncio.sleep(2)
            
            response = await get_client().request("DELETE", f"/api/v0/labs/{lab_id}")
            return f"Lab {lab_id} deleted successfully"
        except Exception as e:
            return f"Error deleting lab: {str(e)}"

    @mcp.tool()
    async def start_lab(lab_id: str) -> str:
        """
        Start the specified lab
        
        Args:
            lab_id: ID of the lab to start
        
        Returns:
            Confirmation message
        """
        return await _start_lab(lab_id)

    @mcp.tool()
    async def stop_lab(lab_id: str) -> str:
        """
        Stop the specified lab
        
        Args:
            lab_id: ID of the lab to stop
        
        Returns:
            Confirmation message
        """
        return await _stop_lab(lab_id)

    @mcp.tool()
    async def wait_for_lab_nodes(lab_id: str, timeout: int = 60) -> str:
        """
        Wait for all nodes in a lab to reach the STARTED state
        
        Args:
            lab_id: ID of the lab
            timeout: Maximum time to wait in seconds (default: 60)
        
        Returns:
            Status message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            # Check if the lab is running
            lab_details = await _get_lab_details(lab_id)
            if not isinstance(lab_details, dict) or lab_details.get("state") != "STARTED":
                return "Lab is not in STARTED state. Start the lab first."
            
            print(f"Waiting for nodes in lab {lab_id} to initialize...", file=sys.stderr)
            
            # Get nodes using internal function
            nodes = await _get_lab_nodes(lab_id)
            if isinstance(nodes, str) and "Error" in nodes:
                return nodes
            
            start_time = asyncio.get_event_loop().time()
            all_ready = False
            
            while not all_ready and (asyncio.get_event_loop().time() - start_time) < timeout:
                all_ready = True
                
                for node_id, node in nodes.items():
                    node_info = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes/{node_id}")
                    node_data = node_info.json()
                    
                    state = node_data.get("state", "UNKNOWN")
                    print(f"Node {node_data.get('label', 'unknown')} state: {state}", file=sys.stderr)
                    
                    if state != "STARTED":
                        all_ready = False
                
                if not all_ready:
                    await asyncio.sleep(5)  # Wait 5 seconds before checking again
            
            if all_ready:
                return "All nodes in the lab are initialized and ready"
            else:
                return f"Timeout reached ({timeout} seconds). Some nodes may not be fully initialized."
        except Exception as e:
            print(f"Error waiting for nodes: {str(e)}", file=sys.stderr)
            return f"Error waiting for nodes: {str(e)}"

    @mcp.tool()
    async def list_node_definitions() -> Union[Dict[str, Any], str]:
        """
        List all available node definitions in CML
        
        Returns:
            Dictionary of available node definitions or error message
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check["error"]
        
        try:
            response = await get_client().request("GET", "/api/v0/node_definitions")
            node_defs = response.json()
            
            # If the response is a list, convert it to a dictionary
            if isinstance(node_defs, list):
                print(f"Converting node definitions list to dictionary", file=sys.stderr)
                result = {}
                for node_def in node_defs:
                    node_id = node_def.get("id")
                    if node_id:
                        result[node_id] = node_def
                return result
            
            # Format the result to be more readable
            result = {}
            for node_id, node_info in node_defs.items():
                result[node_id] = {
                    "description": node_info.get("description", ""),
                    "type": node_info.get("type", ""),
                    "interfaces": node_info.get("interfaces", []),
                }
            
            return result
        except Exception as e:
            return f"Error listing node definitions: {str(e)}"

"""
Topology Handler - FULLY FIXED VERSION

Handles node creation, interface management, and link creation in CML labs.
Now with correct physical interface filtering and working link creation.
"""

import sys
from typing import Dict, Any, Union, Optional, List
from fastmcp import FastMCP

from ..client import get_client
from ..utils import check_auth, handle_api_error


# Actual function implementations (not wrapped as tools)
async def _get_lab_nodes(lab_id: str) -> Union[Dict[str, Any], str]:
    """
    Get all nodes in a specific lab
    
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


async def _add_node(
    lab_id: str, 
    label: str, 
    node_definition: str, 
    x: int = 0, 
    y: int = 0,
    populate_interfaces: bool = True,
    ram: Optional[int] = None,
    cpu_limit: Optional[int] = None,
    parameters: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Add a node to the specified lab
    
    Args:
        lab_id: ID of the lab
        label: Label for the new node
        node_definition: Type of node (e.g., 'iosv', 'csr1000v')
        x: X coordinate for node placement
        y: Y coordinate for node placement
        populate_interfaces: Whether to automatically create interfaces
        ram: RAM allocation for the node (optional)
        cpu_limit: CPU limit for the node (optional)
        parameters: Node-specific parameters (optional)
    
    Returns:
        Dictionary with node ID and confirmation message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check
    
    try:
        # Construct the node data payload
        node_data = {
            "label": label,
            "node_definition": node_definition,
            "x": x,
            "y": y,
            "parameters": parameters or {},
            "tags": [],
            "hide_links": False
        }
        
        # Add optional parameters if provided
        if ram is not None:
            node_data["ram"] = ram
        
        if cpu_limit is not None:
            node_data["cpu_limit"] = cpu_limit
        
        # Add populate_interfaces as a query parameter if needed
        endpoint = f"/api/v0/labs/{lab_id}/nodes"
        if populate_interfaces:
            endpoint += "?populate_interfaces=true"
        
        # Make the API request with explicit Content-Type header
        headers = {"Content-Type": "application/json"}
        response = await get_client().request(
            "POST",
            endpoint,
            json=node_data,
            headers=headers
        )
        
        # Process the response
        result = response.json()
        node_id = result.get("id")
        
        if not node_id:
            return {"error": "Failed to create node, no node ID returned", "response": result}
        
        return {
            "node_id": node_id,
            "message": f"Added node '{label}' with ID: {node_id}",
            "status": "success",
            "details": result
        }
    except Exception as e:
        return handle_api_error("add_node", e)


async def _create_router(lab_id: str, label: str, x: int = 0, y: int = 0) -> Dict[str, Any]:
    """
    Create a router with the 'iosv' node definition
    
    Args:
        lab_id: ID of the lab
        label: Label for the new router
        x: X coordinate for node placement
        y: Y coordinate for node placement
    
    Returns:
        Dictionary with node ID and confirmation message
    """
    return await _add_node(lab_id, label, "iosv", x, y, True)


async def _create_switch(lab_id: str, label: str, x: int = 0, y: int = 0) -> Dict[str, Any]:
    """
    Create a switch with the 'iosvl2' node definition
    
    Args:
        lab_id: ID of the lab
        label: Label for the new switch
        x: X coordinate for node placement
        y: Y coordinate for node placement
    
    Returns:
        Dictionary with node ID and confirmation message
    """
    return await _add_node(lab_id, label, "iosvl2", x, y, True)


async def _get_node_interfaces(lab_id: str, node_id: str) -> Union[List[str], str]:
    """
    Get interfaces for a specific node
    
    Args:
        lab_id: ID of the lab
        node_id: ID of the node
    
    Returns:
        List of interface IDs or error message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/nodes/{node_id}/interfaces")
        interfaces = response.json()
        
        print(f"Got interfaces for node {node_id}: {interfaces}", file=sys.stderr)
        
        # Return the list of interface IDs
        if isinstance(interfaces, list):
            return interfaces
        elif isinstance(interfaces, str):
            # If it's a string, try to parse as space-separated UUIDs
            return interfaces.split()
        else:
            return f"Unexpected interface response format: {type(interfaces)}"
            
    except Exception as e:
        return f"Error getting node interfaces: {str(e)}"


async def _get_physical_interfaces(lab_id: str, node_id: str) -> Union[List[Dict[str, Any]], str]:
    """
    Get all physical interfaces for a specific node (excludes loopback, management, etc.)
    
    Args:
        lab_id: ID of the lab
        node_id: ID of the node
    
    Returns:
        List of physical interfaces or error message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        # First get all interface IDs
        interface_ids = await _get_node_interfaces(lab_id, node_id)
        
        if isinstance(interface_ids, str) and "Error" in interface_ids:
            return interface_ids
        
        if not isinstance(interface_ids, list):
            return f"Expected list of interface IDs, got: {type(interface_ids)}"
        
        # Get details for each interface and filter for physical interfaces
        physical_interfaces = []
        for interface_id in interface_ids:
            try:
                interface_response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/interfaces/{interface_id}")
                interface_data = interface_response.json()
                
                # FIXED: Only include interfaces with type="physical"
                if interface_data.get("type") == "physical":
                    physical_interfaces.append({
                        "id": interface_data["id"],
                        "label": interface_data["label"],
                        "slot": interface_data.get("slot"),
                        "is_connected": interface_data.get("is_connected", False),
                        "mac_address": interface_data.get("mac_address"),
                        "type": interface_data["type"]
                    })
                    
            except Exception as e:
                print(f"Error getting interface {interface_id} details: {str(e)}", file=sys.stderr)
        
        return physical_interfaces if physical_interfaces else f"No physical interfaces found for node {node_id}"
        
    except Exception as e:
        return handle_api_error("get_physical_interfaces", e)


async def _get_lab_links(lab_id: str) -> Union[Dict[str, Any], str]:
    """
    Get all links in a specific lab
    
    Args:
        lab_id: ID of the lab
    
    Returns:
        Dictionary of links in the lab or error message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/links")
        links = response.json()
        
        print(f"Got links: {links}", file=sys.stderr)
        
        # If the response is a list of link IDs, fetch details for each
        if isinstance(links, list):
            result = {}
            for link_id in links:
                try:
                    link_response = await get_client().request("GET", f"/api/v0/labs/{lab_id}/links/{link_id}")
                    link_data = link_response.json()
                    result[link_id] = link_data
                except Exception as e:
                    print(f"Error getting link {link_id} details: {str(e)}", file=sys.stderr)
                    result[link_id] = {"id": link_id}
            return result
        else:
            return links
            
    except Exception as e:
        return f"Error getting lab links: {str(e)}"


async def _find_available_physical_interface(lab_id: str, node_id: str) -> Union[str, Dict[str, str]]:
    """
    Find an available physical interface on a node (FIXED VERSION)
    
    Args:
        lab_id: ID of the lab
        node_id: ID of the node
        
    Returns:
        Interface ID or error dictionary
    """
    try:
        # Get physical interfaces for the node
        physical_interfaces = await _get_physical_interfaces(lab_id, node_id)
        
        if isinstance(physical_interfaces, str):
            return {"error": physical_interfaces}
        
        if not physical_interfaces:
            return {"error": f"No physical interfaces found for node {node_id}"}
        
        # Find first unconnected physical interface
        for interface in physical_interfaces:
            if not interface.get("is_connected", True):  # Default to True to be safe
                return interface.get("id")
        
        # If all are connected, return the first one (might still work)
        if physical_interfaces:
            return physical_interfaces[0].get("id")
        
        return {"error": f"No available physical interfaces found for node {node_id}"}
        
    except Exception as e:
        return handle_api_error("find_available_interface", e)


async def _create_link_v3(lab_id: str, interface_id_a: str, interface_id_b: str) -> Dict[str, Any]:
    """
    Create a link between two interfaces in a lab (FIXED VERSION)
    
    Args:
        lab_id: ID of the lab
        interface_id_a: ID of the first interface (must be physical)
        interface_id_b: ID of the second interface (must be physical)
    
    Returns:
        Dictionary with link ID and confirmation message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check
    
    try:
        print(f"Creating link between interfaces {interface_id_a} and {interface_id_b}", file=sys.stderr)
        
        # Use the correct API format that we verified works
        link_data = {
            "src_int": interface_id_a,
            "dst_int": interface_id_b
        }
        
        headers = {"Content-Type": "application/json"}
        response = await get_client().request(
            "POST", 
            f"/api/v0/labs/{lab_id}/links",
            json=link_data,
            headers=headers
        )
        
        result = response.json()
        print(f"Link creation successful: {result}", file=sys.stderr)
        
        # Extract the link ID from the response
        link_id = result.get("id")
        if not link_id:
            return {"error": "Failed to create link, no link ID returned", "response": result}
        
        return {
            "link_id": link_id,
            "message": f"Created link between interfaces {interface_id_a} and {interface_id_b}",
            "status": "success",
            "details": result
        }
        
    except Exception as e:
        return handle_api_error("create_link", e)


async def _link_nodes(lab_id: str, node_id_a: str, node_id_b: str) -> Dict[str, Any]:
    """
    Create a link between two nodes by automatically selecting available physical interfaces
    
    Args:
        lab_id: ID of the lab
        node_id_a: ID of the first node
        node_id_b: ID of the second node
    
    Returns:
        Dictionary with link ID and confirmation message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check
    
    try:
        # Find available physical interfaces on both nodes
        interface_a = await _find_available_physical_interface(lab_id, node_id_a)
        if isinstance(interface_a, dict) and "error" in interface_a:
            return interface_a
        
        interface_b = await _find_available_physical_interface(lab_id, node_id_b)
        if isinstance(interface_b, dict) and "error" in interface_b:
            return interface_b
        
        # Create the link using these physical interfaces
        return await _create_link_v3(lab_id, interface_a, interface_b)
    except Exception as e:
        return handle_api_error("link_nodes", e)


async def _delete_link(lab_id: str, link_id: str) -> str:
    """
    Delete a link from a lab
    
    Args:
        lab_id: ID of the lab
        link_id: ID of the link to delete
    
    Returns:
        Confirmation message
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        response = await get_client().request("DELETE", f"/api/v0/labs/{lab_id}/links/{link_id}")
        return f"Link {link_id} deleted successfully"
    except Exception as e:
        return f"Error deleting link: {str(e)}"


async def _get_lab_topology(lab_id: str) -> str:
    """
    Get a detailed summary of the lab topology
    
    Args:
        lab_id: ID of the lab
    
    Returns:
        Formatted summary of the lab topology
    """
    auth_check = check_auth()
    if auth_check:
        return auth_check["error"]
    
    try:
        # Get lab details (direct API call to avoid import issues)
        lab_response = await get_client().request("GET", f"/api/v0/labs/{lab_id}")
        lab_details = lab_response.json()
        
        # Get nodes
        nodes = await _get_lab_nodes(lab_id)
        if isinstance(nodes, str) and "Error" in nodes:
            return nodes
        
        # Get links
        links = await _get_lab_links(lab_id)
        if isinstance(links, str) and "Error" in links:
            return links
        
        # Create a topology summary
        result = f"Lab Topology: {lab_details.get('title', 'Untitled')}\n"
        result += f"State: {lab_details.get('state', 'unknown')}\n"
        result += f"Description: {lab_details.get('description', 'None')}\n\n"
        
        # Add nodes
        result += "Nodes:\n"
        if isinstance(nodes, dict):
            for node_id, node in nodes.items():
                result += f"- {node.get('label', 'Unnamed')} (ID: {node_id[:8]}...)\n"
                result += f"  Type: {node.get('node_definition', 'unknown')}\n"
                result += f"  State: {node.get('state', 'unknown')}\n"
        
        # Add links
        result += "\nLinks:\n"
        if isinstance(links, dict):
            if links:
                for link_id, link in links.items():
                    result += f"- Link {link_id[:8]}... between interfaces\n"
                    if "src_int" in link and "dst_int" in link:
                        result += f"  From: {link['src_int'][:8]}... To: {link['dst_int'][:8]}...\n"
            else:
                result += "- No links created yet\n"
        
        return result
    except Exception as e:
        return f"Error getting lab topology: {str(e)}"


def register_topology_tools(mcp: FastMCP):
    """Register topology management tools with the MCP server"""
    
    @mcp.tool()
    async def get_lab_nodes(lab_id: str) -> Union[Dict[str, Any], str]:
        """
        Get all nodes in a specific lab
        
        Args:
            lab_id: ID of the lab
        
        Returns:
            Dictionary of nodes in the lab or error message
        """
        return await _get_lab_nodes(lab_id)

    @mcp.tool()
    async def add_node(
        lab_id: str, 
        label: str, 
        node_definition: str, 
        x: int = 0, 
        y: int = 0,
        populate_interfaces: bool = True,
        ram: Optional[int] = None,
        cpu_limit: Optional[int] = None,
        parameters: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Add a node to the specified lab
        
        Args:
            lab_id: ID of the lab
            label: Label for the new node
            node_definition: Type of node (e.g., 'iosv', 'csr1000v')
            x: X coordinate for node placement
            y: Y coordinate for node placement
            populate_interfaces: Whether to automatically create interfaces
            ram: RAM allocation for the node (optional)
            cpu_limit: CPU limit for the node (optional)
            parameters: Node-specific parameters (optional)
        
        Returns:
            Dictionary with node ID and confirmation message
        """
        return await _add_node(lab_id, label, node_definition, x, y, populate_interfaces, ram, cpu_limit, parameters)

    @mcp.tool()
    async def create_router(
        lab_id: str,
        label: str,
        x: int = 0,
        y: int = 0
    ) -> Dict[str, Any]:
        """
        Create a router with the 'iosv' node definition
        
        Args:
            lab_id: ID of the lab
            label: Label for the new router
            x: X coordinate for node placement
            y: Y coordinate for node placement
        
        Returns:
            Dictionary with node ID and confirmation message
        """
        return await _create_router(lab_id, label, x, y)

    @mcp.tool()
    async def create_switch(
        lab_id: str,
        label: str,
        x: int = 0,
        y: int = 0
    ) -> Dict[str, Any]:
        """
        Create a switch with the 'iosvl2' node definition
        
        Args:
            lab_id: ID of the lab
            label: Label for the new switch
            x: X coordinate for node placement
            y: Y coordinate for node placement
        
        Returns:
            Dictionary with node ID and confirmation message
        """
        return await _create_switch(lab_id, label, x, y)

    @mcp.tool()
    async def get_node_interfaces(lab_id: str, node_id: str) -> Union[List[str], str]:
        """
        Get interfaces for a specific node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
        
        Returns:
            List of interface IDs or error message
        """
        return await _get_node_interfaces(lab_id, node_id)

    @mcp.tool()
    async def get_physical_interfaces(lab_id: str, node_id: str) -> Union[List[Dict[str, Any]], str]:
        """
        Get all physical interfaces for a specific node (excludes loopback, management, etc.)
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
        
        Returns:
            List of physical interfaces or error message
        """
        return await _get_physical_interfaces(lab_id, node_id)

    @mcp.tool()
    async def get_lab_links(lab_id: str) -> Union[Dict[str, Any], str]:
        """
        Get all links in a specific lab
        
        Args:
            lab_id: ID of the lab
        
        Returns:
            Dictionary of links in the lab or error message
        """
        return await _get_lab_links(lab_id)

    @mcp.tool()
    async def create_link_v3(lab_id: str, interface_id_a: str, interface_id_b: str) -> Dict[str, Any]:
        """
        Create a link between two interfaces in a lab (FIXED VERSION)
        
        Args:
            lab_id: ID of the lab
            interface_id_a: ID of the first interface (must be physical)
            interface_id_b: ID of the second interface (must be physical)
        
        Returns:
            Dictionary with link ID and confirmation message
        """
        return await _create_link_v3(lab_id, interface_id_a, interface_id_b)

    @mcp.tool()
    async def link_nodes(lab_id: str, node_id_a: str, node_id_b: str) -> Dict[str, Any]:
        """
        Create a link between two nodes by automatically selecting available physical interfaces
        
        Args:
            lab_id: ID of the lab
            node_id_a: ID of the first node
            node_id_b: ID of the second node
        
        Returns:
            Dictionary with link ID and confirmation message
        """
        return await _link_nodes(lab_id, node_id_a, node_id_b)

    @mcp.tool()
    async def delete_link(lab_id: str, link_id: str) -> str:
        """
        Delete a link from a lab
        
        Args:
            lab_id: ID of the lab
            link_id: ID of the link to delete
        
        Returns:
            Confirmation message
        """
        return await _delete_link(lab_id, link_id)

    @mcp.tool()
    async def get_lab_topology(lab_id: str) -> str:
        """
        Get a detailed summary of the lab topology
        
        Args:
            lab_id: ID of the lab
        
        Returns:
            Formatted summary of the lab topology
        """
        return await _get_lab_topology(lab_id)

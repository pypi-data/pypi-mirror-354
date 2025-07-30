"""
Console Handler

Handles console session management and command execution in CML labs.
"""

from typing import Dict, Any, List
from fastmcp import FastMCP

from client import get_client
from utils import check_auth


def register_console_tools(mcp: FastMCP):
    """Register console management tools with the MCP server"""
    
    @mcp.tool()
    async def open_console_session(lab_id: str, node_id: str) -> Dict[str, Any]:
        """
        Open a console session to a node in the lab
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node to access
        
        Returns:
            Dictionary with session information
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            response = await get_client().request("POST", f"/api/v0/labs/{lab_id}/nodes/{node_id}/console")
            session_info = response.json()
            return {
                "status": "success",
                "message": f"Console session opened for node {node_id}",
                "session_info": session_info
            }
        except Exception as e:
            return {"error": f"Error opening console session: {str(e)}"}

    @mcp.tool()
    async def close_console_session(lab_id: str, node_id: str) -> Dict[str, Any]:
        """
        Close a console session to a node in the lab
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node with an open session
        
        Returns:
            Dictionary with operation status
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            response = await get_client().request("DELETE", f"/api/v0/labs/{lab_id}/nodes/{node_id}/console")
            return {
                "status": "success",
                "message": f"Console session closed for node {node_id}"
            }
        except Exception as e:
            return {"error": f"Error closing console session: {str(e)}"}

    @mcp.tool()
    async def send_console_command(lab_id: str, node_id: str, command: str) -> Dict[str, Any]:
        """
        Send a command to a node console
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
            command: Command to send
        
        Returns:
            Dictionary with command output
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            response = await get_client().request(
                "POST",
                f"/api/v0/labs/{lab_id}/nodes/{node_id}/console/command",
                json={"command": command}
            )
            
            result = response.json()
            return {
                "status": "success",
                "command": command,
                "output": result.get("output", ""),
                "details": result
            }
        except Exception as e:
            return {"error": f"Error sending console command: {str(e)}"}

    @mcp.tool()
    async def send_multiple_commands(lab_id: str, node_id: str, commands: List[str]) -> Dict[str, Any]:
        """
        Send multiple commands to a node console
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
            commands: List of commands to send
        
        Returns:
            Dictionary with command outputs
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            results = []
            for command in commands:
                command_result = await send_console_command(lab_id, node_id, command)
                results.append(command_result)
            
            return {
                "status": "success",
                "commands_sent": len(commands),
                "results": results
            }
        except Exception as e:
            return {"error": f"Error sending multiple commands: {str(e)}"}

    @mcp.tool()
    async def check_interfaces(lab_id: str, node_id: str, interface_name: str = None) -> Dict[str, Any]:
        """
        Check interface status on a node
        
        Args:
            lab_id: ID of the lab
            node_id: ID of the node
            interface_name: Optional specific interface to check (check all if not specified)
        
        Returns:
            Dictionary with interface status
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            if interface_name:
                command = f"show interfaces {interface_name}"
            else:
                command = "show interfaces brief"
            
            result = await send_console_command(lab_id, node_id, command)
            
            return {
                "status": "success",
                "interface_check": interface_name or "all interfaces",
                "output": result.get("output", ""),
                "command_used": command
            }
        except Exception as e:
            return {"error": f"Error checking interfaces: {str(e)}"}

    @mcp.tool()
    async def get_diagnostic_recommendations(lab_id: str, report_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get recommendations based on a troubleshooting report
        
        Args:
            lab_id: ID of the lab
            report_data: Optional report data from a previous troubleshooting run
        
        Returns:
            Dictionary with recommendations
        """
        auth_check = check_auth()
        if auth_check:
            return auth_check
        
        try:
            # Import here to avoid circular imports
            from topology import _get_lab_topology
            
            # Get current lab topology
            topology = await _get_lab_topology(lab_id)
            
            recommendations = [
                "1. Verify all nodes are in STARTED state",
                "2. Check interface status using 'show interfaces brief'",
                "3. Verify IP addressing and subnet configuration",
                "4. Test connectivity with ping commands",
                "5. Check routing tables with 'show ip route'",
                "6. Verify VLAN configuration on switches if applicable"
            ]
            
            # Add specific recommendations based on report data if provided
            if report_data:
                if "connectivity_issues" in report_data:
                    recommendations.append("7. Focus on Layer 2/3 connectivity troubleshooting")
                if "routing_issues" in report_data:
                    recommendations.append("8. Review routing protocol configuration and neighbor relationships")
            
            return {
                "status": "success",
                "lab_id": lab_id,
                "recommendations": recommendations,
                "topology_summary": topology,
                "report_data": report_data or "No previous report data provided"
            }
        except Exception as e:
            return {"error": f"Error generating diagnostic recommendations: {str(e)}"}

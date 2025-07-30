"""
Handler modules for CML MCP Server

This package contains modular handlers for different aspects of CML management.
"""

from .lab_management import register_lab_management_tools
from .topology import register_topology_tools
from .configuration import register_configuration_tools
from .console import register_console_tools

__all__ = [
    'register_lab_management_tools',
    'register_topology_tools', 
    'register_configuration_tools',
    'register_console_tools'
]

"""
CML API Client

Handles authentication and HTTP requests to the Cisco Modeling Labs API.
"""

import os
import sys
import httpx
import traceback
from typing import Optional


class CMLAuth:
    """Authentication and request handling for Cisco Modeling Labs"""
    
    def __init__(self, base_url: str, username: str, password: str, verify_ssl: bool = True):
        """
        Initialize the CML authentication client
        
        Args:
            base_url: Base URL of the CML server
            username: Username for CML authentication
            password: Password for CML authentication
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = None
        self.verify_ssl = verify_ssl
        self.client = httpx.AsyncClient(base_url=base_url, verify=verify_ssl)
        
        # Suppress SSL warnings if verify_ssl is False
        if not verify_ssl:
            try:
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            except ImportError:
                print("urllib3 not available, SSL warning suppression disabled", file=sys.stderr)
    
    async def authenticate(self) -> str:
        """
        Authenticate with CML and get a token
        
        Returns:
            Authentication token
        
        Raises:
            httpx.HTTPStatusError: If authentication fails
        """
        print(f"Authenticating with CML at {self.base_url}", file=sys.stderr)
        response = await self.client.post(
            "/api/v0/authenticate",
            json={"username": self.username, "password": self.password}
        )
        response.raise_for_status()
        self.token = response.text.strip('"')  # Remove any quotes from the token
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})
        
        # Verify the token works
        try:
            auth_check = await self.client.get("/api/v0/authok")
            auth_check.raise_for_status()
            print(f"Authentication successful, token verified", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Token verification failed: {str(e)}", file=sys.stderr)
            
        return self.token
    
    async def request(self, method: str, endpoint: str, **kwargs) -> httpx.Response:
        """
        Make an authenticated request to CML API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint to call
            **kwargs: Additional arguments to pass to httpx
        
        Returns:
            HTTP response
            
        Raises:
            httpx.HTTPStatusError: If the request fails
        """
        if not self.token:
            await self.authenticate()
        
        # Print debug info to help troubleshoot
        print(f"Making {method} request to {endpoint}", file=sys.stderr)
        
        # Ensure headers contain the token
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        
        # Ensure the Authorization header is set with the current token
        kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
        
        # Make the request
        try:
            response = await self.client.request(method, endpoint, **kwargs)
            
            # If unauthorized, try to re-authenticate once
            if response.status_code == 401:
                print(f"Got 401 response, re-authenticating...", file=sys.stderr)
                await self.authenticate()
                kwargs["headers"]["Authorization"] = f"Bearer {self.token}"
                response = await self.client.request(method, endpoint, **kwargs)
            
            response.raise_for_status()
            return response
        except Exception as e:
            print(f"Request error: {str(e)}", file=sys.stderr)
            raise


# Global state for CML client
cml_auth: Optional[CMLAuth] = None


def get_client() -> Optional[CMLAuth]:
    """Get the current CML client instance"""
    return cml_auth


def set_client(client: CMLAuth) -> None:
    """Set the CML client instance"""
    global cml_auth
    cml_auth = client

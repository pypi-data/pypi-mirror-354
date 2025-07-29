"""
Authentication module for doc2mcp SDK
Provides login/logout functionality similar to wandb
"""

import os
import json
import getpass
from pathlib import Path
from typing import Optional
from .exceptions import APIError

class AuthManager:
    """Manages authentication for the doc2mcp SDK"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".doc2mcp"
        self.config_file = self.config_dir / "config.json"
        self.ensure_config_dir()
    
    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(exist_ok=True)
    
    def save_api_key(self, api_key: str, server_url: str):
        """Save API key to config file"""
        config = self.load_config()
        config["api_key"] = api_key
        config["server_url"] = server_url
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Set restrictive permissions for security
        self.config_file.chmod(0o600)
    
    def load_config(self) -> dict:
        """Load configuration from file"""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    
    def get_api_key(self) -> Optional[str]:
        """Get stored API key"""
        config = self.load_config()
        return config.get("api_key")
    
    def get_server_url(self) -> Optional[str]:
        """Get stored server URL"""
        config = self.load_config()
        return config.get("server_url")
    
    def clear_credentials(self):
        """Remove stored credentials"""
        if self.config_file.exists():
            self.config_file.unlink()
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.get_api_key() is not None


def login(server_url: str = "http://localhost:5000", api_key: Optional[str] = None):
    """
    Log in to doc2mcp server
    
    Args:
        server_url: Server URL to connect to
        api_key: API key (if not provided, will prompt)
    """
    auth = AuthManager()
    
    if not api_key:
        print(f"Logging in to doc2mcp server: {server_url}")
        print("\nTo get your API key:")
        print("1. Open the doc2mcp web interface")
        print("2. Go to Settings -> SDK Settings")
        print("3. Generate or copy your API key")
        print()
        
        api_key = getpass.getpass("Enter your API key: ").strip()
    
    if not api_key:
        raise ValueError("API key is required")
    
    # Test the API key by attempting to list projects
    from .client import Doc2MCPClient
    
    try:
        client = Doc2MCPClient(server_url, api_key=api_key)
        projects = client.get_projects()
        
        # Save credentials if successful
        auth.save_api_key(api_key, server_url)
        
        print(f"✓ Successfully logged in to {server_url}")
        print(f"✓ Found {len(projects)} projects in your workspace")
        
    except Exception as e:
        if "401" in str(e) or "Unauthorized" in str(e):
            raise APIError("Invalid API key. Please check your credentials.", 401)
        else:
            raise APIError(f"Failed to connect to server: {e}")


def logout():
    """Log out from doc2mcp"""
    auth = AuthManager()
    
    if not auth.is_logged_in():
        print("Not currently logged in")
        return
    
    auth.clear_credentials()
    print("✓ Successfully logged out")


def whoami():
    """Show current login status"""
    auth = AuthManager()
    
    if not auth.is_logged_in():
        print("Not logged in")
        print("\nRun 'doc2mcp login' to authenticate")
        return
    
    server_url = auth.get_server_url()
    print(f"Logged in to: {server_url}")
    
    try:
        from .client import Doc2MCPClient
        if server_url:
            client = Doc2MCPClient(server_url, api_key=auth.get_api_key())
            projects = client.get_projects()
            print(f"Workspace contains {len(projects)} projects")
    except Exception as e:
        print(f"Warning: Could not verify connection - {e}")


def get_authenticated_client(server_url: Optional[str] = None):
    """
    Get an authenticated client instance
    
    Args:
        server_url: Override server URL
        
    Returns:
        Authenticated Doc2MCPClient
        
    Raises:
        APIError: If not logged in or invalid credentials
    """
    from .client import Doc2MCPClient
    
    auth = AuthManager()
    
    if not auth.is_logged_in():
        raise APIError(
            "Not logged in. Run 'doc2mcp login' to authenticate.",
            401
        )
    
    api_key = auth.get_api_key()
    if not server_url:
        server_url = auth.get_server_url()
    
    if not server_url:
        raise APIError("No server URL configured. Please log in again.", 401)
    
    # Ensure server_url is not None for type checking
    final_server_url: str = server_url
    return Doc2MCPClient(final_server_url, api_key=api_key)
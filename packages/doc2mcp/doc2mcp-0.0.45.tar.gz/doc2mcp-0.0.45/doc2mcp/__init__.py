"""
doc2mcp Python SDK

A Python client for the doc2mcp service that converts documentation into 
MCP-compliant API endpoints for use with Claude, GPT, and other AI assistants.
"""

from .client import Doc2MCPClient
from .exceptions import Doc2MCPError, ProjectNotFoundError, UploadError
from .models import Project, ProjectStatus, DocumentChunk

__version__ = "0.1.0"
__all__ = [
    "Doc2MCPClient",
    "Doc2MCPError", 
    "ProjectNotFoundError",
    "UploadError",
    "Project",
    "ProjectStatus", 
    "DocumentChunk"
]
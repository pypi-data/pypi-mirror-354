"""
Exception classes for the doc2mcp SDK
"""


class Doc2MCPError(Exception):
    """Base exception for doc2mcp SDK errors"""
    pass


class ProjectNotFoundError(Doc2MCPError):
    """Raised when a project is not found"""
    pass


class UploadError(Doc2MCPError):
    """Raised when file upload fails"""
    pass


class APIError(Doc2MCPError):
    """Raised when API request fails"""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code
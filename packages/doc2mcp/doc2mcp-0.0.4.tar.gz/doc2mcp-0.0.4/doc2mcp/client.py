"""
Main client for the doc2mcp SDK
"""

import os
import requests
from pathlib import Path
from typing import List, Optional, Union
from urllib.parse import urljoin

from .models import Project, SearchResult, DocumentChunk
from .exceptions import Doc2MCPError, ProjectNotFoundError, UploadError, APIError


class Doc2MCPClient:
    """
    Client for interacting with the doc2mcp service
    
    Example:
        >>> client = Doc2MCPClient("https://your-doc2mcp-instance.com")
        >>> project = client.upload_documents(
        ...     name="My API Docs",
        ...     files=["./docs/api.md", "./docs/guide.md"],
        ...     description="Complete API documentation"
        ... )
        >>> results = client.search(project.slug, "authentication")
    """
    
    def __init__(self, base_url: str = "http://localhost:5000", api_key: Optional[str] = None):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the doc2mcp service
            api_key: SDK API key for authenticated requests (required for user-specific deployment)
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}'
            })
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Make an HTTP request with error handling"""
        url = urljoin(self.base_url, endpoint)
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    message = error_data.get('error', f'HTTP {response.status_code}')
                except:
                    message = f'HTTP {response.status_code}'
                
                if response.status_code == 404:
                    raise ProjectNotFoundError(message)
                else:
                    raise APIError(message, response.status_code)
            return response
        except requests.RequestException as e:
            raise Doc2MCPError(f"Request failed: {e}")
    
    def upload_documents(
        self, 
        name: str, 
        files: List[Union[str, Path]], 
        description: str = ""
    ) -> Project:
        """
        Upload documents and create a new project
        
        Args:
            name: Name for the project
            files: List of file paths to upload
            description: Optional project description
            
        Returns:
            Created project
            
        Raises:
            UploadError: If upload fails
            Doc2MCPError: If request fails
        """
        try:
            # Prepare files for upload
            files_data = []
            for file_path in files:
                path = Path(file_path)
                if not path.exists():
                    raise UploadError(f"File not found: {file_path}")
                files_data.append(('files', (path.name, open(path, 'rb'))))
            
            # Prepare form data
            form_data = {
                'name': name,
                'description': description
            }
            
            response = self._make_request(
                'POST', 
                '/api/projects',
                data=form_data,
                files=files_data
            )
            
            # Close file handles
            for _, (_, file_handle) in files_data:
                file_handle.close()
                
            return Project.from_dict(response.json())
            
        except Exception as e:
            if isinstance(e, (Doc2MCPError, ProjectNotFoundError, APIError)):
                raise
            raise UploadError(f"Upload failed: {e}")
    
    def get_projects(self) -> List[Project]:
        """
        Get all projects
        
        Returns:
            List of projects
        """
        response = self._make_request('GET', '/api/projects')
        return [Project.from_dict(data) for data in response.json()]
    
    def get_project(self, project_id: int) -> Project:
        """
        Get a specific project by ID
        
        Args:
            project_id: Project ID
            
        Returns:
            Project data
            
        Raises:
            ProjectNotFoundError: If project not found
        """
        response = self._make_request('GET', f'/api/projects/{project_id}')
        return Project.from_dict(response.json())
    
    def delete_project(self, project_id: int) -> bool:
        """
        Delete a project
        
        Args:
            project_id: Project ID to delete
            
        Returns:
            True if successful
            
        Raises:
            ProjectNotFoundError: If project not found
        """
        self._make_request('DELETE', f'/api/projects/{project_id}')
        return True
    
    def search(self, project_slug: str, query: str, api_token: str, limit: int = 10) -> SearchResult:
        """
        Search documents in a project using the MCP endpoint
        
        Args:
            project_slug: Project slug
            query: Search query
            api_token: API token for authentication
            limit: Maximum number of results
            
        Returns:
            Search results
            
        Raises:
            ProjectNotFoundError: If project not found
            APIError: If authentication fails
        """
        params = {'q': query, 'limit': limit}
        headers = {'Authorization': f'Bearer {api_token}'}
        response = self._make_request(
            'GET', 
            f'/api/mcp/{project_slug}/search',
            params=params,
            headers=headers
        )
        return SearchResult.from_dict(response.json())
    
    def get_mcp_endpoint(self, project_slug: str) -> str:
        """
        Get the full MCP endpoint URL for a project
        
        Args:
            project_slug: Project slug
            
        Returns:
            Full MCP endpoint URL
        """
        return f"{self.base_url}/api/mcp/{project_slug}/search"
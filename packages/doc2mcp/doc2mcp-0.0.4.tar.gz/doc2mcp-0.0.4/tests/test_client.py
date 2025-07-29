"""
Tests for the doc2mcp client
"""

import pytest
from unittest.mock import Mock, patch
from doc2mcp.client import Doc2MCPClient
from doc2mcp.models import Project, ProjectStatus
from doc2mcp.exceptions import Doc2MCPError, ProjectNotFoundError


class TestDoc2MCPClient:
    """Test cases for Doc2MCPClient"""

    def test_client_initialization(self):
        """Test client initialization with default values"""
        client = Doc2MCPClient()
        assert client.base_url == "http://localhost:5000"
        assert client.api_key is None

    def test_client_initialization_with_custom_values(self):
        """Test client initialization with custom values"""
        client = Doc2MCPClient(
            base_url="https://example.com",
            api_key="test-key"
        )
        assert client.base_url == "https://example.com"
        assert client.api_key == "test-key"

    @patch('doc2mcp.client.requests.get')
    def test_get_projects_success(self, mock_get):
        """Test successful project retrieval"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "id": 1,
                "name": "Test Project",
                "slug": "test-project",
                "description": "Test description",
                "file_count": 5,
                "status": "ready",
                "created_at": "2024-01-01T00:00:00Z",
                "mcp_endpoint": "http://localhost:5000/mcp/test-project",
                "api_token": "test-token"
            }
        ]
        mock_get.return_value = mock_response

        client = Doc2MCPClient()
        projects = client.get_projects()

        assert len(projects) == 1
        assert projects[0].name == "Test Project"
        assert projects[0].slug == "test-project"

    @patch('doc2mcp.client.requests.get')
    def test_get_projects_error(self, mock_get):
        """Test project retrieval error handling"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        client = Doc2MCPClient()
        
        with pytest.raises(Doc2MCPError):
            client.get_projects()

    def test_get_mcp_endpoint(self):
        """Test MCP endpoint URL generation"""
        client = Doc2MCPClient("https://api.example.com")
        endpoint = client.get_mcp_endpoint("my-project")
        
        assert endpoint == "https://api.example.com/mcp/my-project"
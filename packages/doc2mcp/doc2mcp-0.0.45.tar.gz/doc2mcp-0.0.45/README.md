# doc2mcp Python SDK

Python client library for the doc2mcp service that converts documentation into MCP-compliant API endpoints.

## Installation

```bash
pip install doc2mcp
```

## Quick Start

### Authentication

First, authenticate with your doc2mcp server:

```python
from doc2mcp import login

# Login to your doc2mcp instance
login("https://your-doc2mcp-instance.com")
```

### Upload Documentation

```python
from doc2mcp import Doc2MCPClient

# Initialize authenticated client
client = Doc2MCPClient()

# Upload documentation files
project = client.upload_documents(
    name="My API Documentation",
    files=["./docs/api.md", "./docs/guide.md", "./README.md"],
    description="Complete API documentation for my project"
)

print(f"Project created: {project.name}")
print(f"MCP Endpoint: {project.mcp_endpoint}")
print(f"API Token: {project.api_token}")
```

### Search Documents

```python
# Search your documentation
results = client.search(
    project_slug=project.slug,
    query="authentication setup",
    api_token=project.api_token,
    limit=5
)

for result in results.results:
    print(f"Score: {result.score}")
    print(f"Content: {result.content[:200]}...")
```

### List Projects

```python
# Get all your projects
projects = client.get_projects()

for project in projects:
    print(f"{project.name} ({project.status}) - {project.file_count} files")
```

## CLI Usage

The SDK includes a command-line interface:

### Authentication

```bash
# Login
doc2mcp login --server https://your-instance.com

# Check login status
doc2mcp whoami

# Logout
doc2mcp logout
```

### Project Management

```bash
# Upload documentation
doc2mcp upload --name "My Docs" --description "API documentation" ./docs/

# List projects
doc2mcp list

# Search in a project
doc2mcp search my-project-slug "authentication"

# Delete a project
doc2mcp delete my-project-slug
```

## API Reference

### Client Class

```python
from doc2mcp import Doc2MCPClient

client = Doc2MCPClient(
    base_url="https://your-instance.com",  # Optional, uses authenticated server
    api_key="your-api-key"  # Optional, uses stored credentials
)
```

### Methods

#### `upload_documents(name, files, description="")`

Upload documentation files and create a new project.

**Parameters:**
- `name` (str): Project name
- `files` (List[str]): List of file paths to upload
- `description` (str, optional): Project description

**Returns:** `Project` object with endpoint details

#### `get_projects()`

Get all projects for the authenticated user.

**Returns:** List of `Project` objects

#### `get_project(project_id)`

Get a specific project by ID.

**Parameters:**
- `project_id` (int): Project ID

**Returns:** `Project` object

#### `delete_project(project_id)`

Delete a project and its MCP endpoint.

**Parameters:**
- `project_id` (int): Project ID to delete

**Returns:** Boolean indicating success

#### `search(project_slug, query, api_token, limit=10)`

Search documents in a project using the MCP endpoint.

**Parameters:**
- `project_slug` (str): Project slug
- `query` (str): Search query
- `api_token` (str): API token for authentication
- `limit` (int, optional): Maximum number of results

**Returns:** `SearchResult` object with matching documents

### Data Models

#### Project

```python
@dataclass
class Project:
    id: int
    name: str
    slug: str
    description: str
    status: str  # 'processing', 'ready', 'error'
    file_count: int
    mcp_endpoint: str
    api_token: str
    created_at: str
```

#### SearchResult

```python
@dataclass
class SearchResult:
    results: List[SearchResultItem]
    total: int
    query: str

@dataclass
class SearchResultItem:
    content: str
    score: float
    metadata: dict
```

## Error Handling

```python
from doc2mcp.exceptions import (
    Doc2MCPError,
    ProjectNotFoundError,
    UploadError,
    APIError
)

try:
    project = client.upload_documents(
        name="My Docs",
        files=["./nonexistent.md"]
    )
except UploadError as e:
    print(f"Upload failed: {e}")
except APIError as e:
    print(f"API error: {e}")
```

## Configuration

The SDK stores configuration in `~/.config/doc2mcp/config.json`:

```json
{
    "server_url": "https://your-instance.com",
    "api_key": "your-api-key"
}
```

## Contributing

1. Clone the repository
2. Install in development mode: `pip install -e .`
3. Run tests: `pytest tests/`
4. Follow the contribution guidelines in CONTRIBUTING.md

## Author

Created by [Yacine Zahidi](https://yacinezahidi.com) ([@ell-hol](https://github.com/ell-hol))

## License

MIT License - see LICENSE file for details
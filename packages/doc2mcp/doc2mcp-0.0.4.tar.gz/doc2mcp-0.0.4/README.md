# doc2mcp Python SDK

[![PyPI version](https://badge.fury.io/py/doc2mcp.svg)](https://badge.fury.io/py/doc2mcp)
[![Python Support](https://img.shields.io/pypi/pyversions/doc2mcp.svg)](https://pypi.org/project/doc2mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python SDK for converting documentation into MCP-compliant API endpoints that work seamlessly with Claude, GPT, and other AI assistants.

## Quick Start

### Installation

```bash
pip install doc2mcp
```

### Basic Usage

```python
from doc2mcp import Doc2MCPClient

# Initialize client with your API key
client = Doc2MCPClient(
    base_url="https://your-doc2mcp-instance.com",
    api_key="sdk_your_api_key_here"  # Get this from your dashboard
)

# Upload documentation
project = client.upload_documents(
    name="My API Documentation",
    files=["./docs/api.md", "./docs/guide.md"],
    description="Complete API documentation with examples"
)

print(f"Project created: {project.name}")
print(f"MCP Endpoint: {project.mcp_endpoint}")
print(f"API Token: {project.api_token}")
```

### CLI Usage

```bash
# Upload documents
doc2mcp upload --name "My Docs" --files docs/*.md

# List projects
doc2mcp list

# Search project
doc2mcp search my-project-slug "authentication"

# Delete project
doc2mcp delete 123
```

## Features

- **Authenticated Deployment**: Projects are automatically associated with your user account
- **Multiple File Support**: Upload Markdown, HTML, PDF, and text files
- **Semantic Search**: Built-in embedding-based search using OpenAI
- **MCP Compliance**: Generate endpoints that work with Claude Desktop, GPT, and other AI tools
- **Real-time Processing**: LangChain-powered text splitting and chunking
- **Connection Tracking**: Monitor how often your endpoints are accessed

## Authentication

### Getting Your API Key

1. Log in to your doc2mcp dashboard
2. Navigate to SDK Settings
3. Generate a new API key
4. Use the key in your Python code

### Environment Variables

Set your API key as an environment variable:

```bash
export DOC2MCP_API_KEY="sdk_your_api_key_here"
```

Then use it in code:

```python
import os
from doc2mcp import Doc2MCPClient

client = Doc2MCPClient(
    base_url="https://your-instance.com",
    api_key=os.getenv("DOC2MCP_API_KEY")
)
```

## Advanced Usage

### Batch Operations

```python
# Upload multiple project sets
projects = []
for doc_set in ["api-docs", "user-guides", "tutorials"]:
    project = client.upload_documents(
        name=f"Documentation - {doc_set.title()}",
        files=[f"./docs/{doc_set}/*.md"],
        description=f"Complete {doc_set} documentation"
    )
    projects.append(project)

# Search across projects
for project in projects:
    results = client.search(project.slug, "authentication", project.api_token)
    print(f"Found {len(results.chunks)} results in {project.name}")
```

### Error Handling

```python
from doc2mcp import Doc2MCPClient, UploadError, ProjectNotFoundError

try:
    project = client.upload_documents(
        name="My Docs",
        files=["./docs/guide.md"],
        description="User guide"
    )
except UploadError as e:
    print(f"Upload failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## API Reference

### Doc2MCPClient

#### `__init__(base_url, api_key=None)`

Initialize the client.

**Parameters:**
- `base_url` (str): Base URL of your doc2mcp instance
- `api_key` (str, optional): SDK API key for authenticated requests

#### `upload_documents(name, files, description="")`

Upload documents and create a new project.

**Parameters:**
- `name` (str): Project name
- `files` (List[str]): List of file paths to upload
- `description` (str): Optional project description

**Returns:** `Project` object

#### `get_projects()`

Get all your projects.

**Returns:** List of `Project` objects

#### `search(project_slug, query, api_token, limit=10)`

Search documents in a project.

**Parameters:**
- `project_slug` (str): Project slug
- `query` (str): Search query
- `api_token` (str): Project API token
- `limit` (int): Maximum results (default: 10)

**Returns:** `SearchResult` object

#### `delete_project(project_id)`

Delete a project.

**Parameters:**
- `project_id` (int): Project ID to delete

**Returns:** `bool` - True if successful

### Models

#### Project

```python
@dataclass
class Project:
    id: int
    name: str
    slug: str
    description: str
    file_count: int
    status: ProjectStatus
    created_at: datetime
    mcp_endpoint: str
    api_token: str
```

#### SearchResult

```python
@dataclass
class SearchResult:
    chunks: list[DocumentChunk]
```

#### DocumentChunk

```python
@dataclass
class DocumentChunk:
    id: str
    content: str
    metadata: Dict[str, Any]
```

## CLI Reference

### Global Options

- `--api-key`: SDK API key (or set DOC2MCP_API_KEY)
- `--base-url`: Base URL of doc2mcp instance
- `--help`: Show help message

### Commands

#### `upload`

Upload documentation files.

```bash
doc2mcp upload --name "Project Name" --files docs/*.md --description "Optional description"
```

**Options:**
- `--name` (required): Project name
- `--files` (required): File paths to upload
- `--description`: Project description

#### `list`

List all your projects.

```bash
doc2mcp list
```

#### `search`

Search within a project.

```bash
doc2mcp search PROJECT_SLUG "search query"
```

**Arguments:**
- `PROJECT_SLUG`: Project slug to search in
- `QUERY`: Search query string

#### `delete`

Delete a project.

```bash
doc2mcp delete PROJECT_ID
```

**Arguments:**
- `PROJECT_ID`: ID of project to delete

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Documentation: https://doc2mcp.com/docs
- Issues: https://github.com/doc2mcp/python-sdk/issues
- Email: support@doc2mcp.com
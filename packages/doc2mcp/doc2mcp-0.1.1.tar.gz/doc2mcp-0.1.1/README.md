# doc2mcp

A Python SDK for the doc2mcp documentation-to-MCP platform.

## Overview

`doc2mcp` is a platform that allows users to upload documentation (Markdown, HTML, PDFs, etc.), which is parsed, chunked, embedded, and exposed via an **MCP-compliant search endpoint**.

This SDK provides a simulated interface to the doc2mcp cloud service for development and testing purposes.

## Installation

```bash
pip install doc2mcp
```

## Usage

### Upload Documentation

```python
import doc2mcp

# Upload documentation to the platform
endpoint = doc2mcp.upload("/path/to/docs", "My Project")
print(f"MCP endpoint: {endpoint}")
# Output: https://api.doc2mcp.dev/mcp/my-project/search
```

### Search Documentation

```python
# Search through uploaded documentation
results = doc2mcp.search("my-project", "authentication")
print(f"Found {len(results['chunks'])} results")

# Access search results
for chunk in results['chunks']:
    print(f"Source: {chunk['metadata']['source']}")
    print(f"Content: {chunk['content']}")
```

### List Projects

```python
# List all uploaded projects
projects = doc2mcp.list_projects()
print(f"Uploaded projects: {projects}")
```

## API Reference

### `upload(path: str, project_name: str) -> str`

Uploads documentation to the doc2mcp platform.

**Parameters:**
- `path`: Path to the local folder or .zip file containing documentation
- `project_name`: Human-readable name for the project

**Returns:**
- The MCP endpoint URL for searching the uploaded documentation

### `search(project_slug: str, query: str) -> dict`

Searches documentation in a doc2mcp project.

**Parameters:**
- `project_slug`: The project slug (generated during upload)
- `query`: The search query string

**Returns:**
- A dictionary containing search results with chunks of relevant content

### `list_projects() -> list[str]`

Lists all uploaded projects.

**Returns:**
- A list of project slugs that have been uploaded in this session

## Example

```python
import doc2mcp

# Upload documentation
endpoint = doc2mcp.upload("/docs/api", "API Documentation")

# Search for specific topics
auth_results = doc2mcp.search("api-documentation", "authentication")
config_results = doc2mcp.search("api-documentation", "configuration")

# List all projects
projects = doc2mcp.list_projects()
print(f"Available projects: {projects}")
```

## Development

This is currently a mock implementation for reserving the package name and testing the API design. The actual doc2mcp service backend is under development.

## License

Apache 2.0 License - see [LICENSE](LICENSE) file for details.

## Author

Yacine Zahidi - [yacinezahidi.com](https://yacinezahidi.com)
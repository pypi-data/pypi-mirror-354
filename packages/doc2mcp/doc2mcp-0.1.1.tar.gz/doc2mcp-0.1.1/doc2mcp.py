"""
doc2mcp SDK - Python SDK for the doc2mcp documentation-to-MCP platform.

This SDK provides a simulated interface to the doc2mcp cloud service,
which allows users to upload documentation and search it via MCP-compliant endpoints.
"""

import re
import json
import time
from typing import Dict, List, Any


# In-memory storage for uploaded project slugs
_uploaded_projects: List[str] = []


def _generate_slug(project_name: str) -> str:
    """
    Generate a URL-safe slug from a project name.
    
    Args:
        project_name: The original project name
        
    Returns:
        A lowercase, URL-safe slug
    """
    # Convert to lowercase and replace spaces/special chars with hyphens
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', project_name.lower())
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug


def upload(path: str, project_name: str) -> str:
    """
    Upload documentation to the doc2mcp platform.
    
    This function simulates uploading a local folder or .zip file of documentation
    to the doc2mcp cloud service. The documentation would be parsed, chunked,
    embedded, and made available via an MCP-compliant search endpoint.
    
    Args:
        path: Path to the local folder or .zip file containing documentation
        project_name: Human-readable name for the project
        
    Returns:
        The MCP endpoint URL for searching the uploaded documentation
        
    Example:
        >>> endpoint = upload("/path/to/docs", "My Project")
        >>> print(endpoint)
        https://api.doc2mcp.dev/mcp/my-project/search
    """
    # Generate slug from project name
    slug = _generate_slug(project_name)
    
    # Store the uploaded project slug
    _uploaded_projects.append(slug)
    
    # Simulate upload process
    print(f"[doc2mcp] Uploading documentation from: {path}")
    print(f"[doc2mcp] Project name: {project_name}")
    print(f"[doc2mcp] Generated slug: {slug}")
    print(f"[doc2mcp] Processing and chunking documents...")
    print(f"[doc2mcp] Creating embeddings...")
    print(f"[doc2mcp] Upload complete!")
    
    # Return the fake MCP endpoint
    endpoint = f"https://api.doc2mcp.dev/mcp/{slug}/search"
    print(f"[doc2mcp] MCP endpoint available at: {endpoint}")
    
    return endpoint


def search(project_slug: str, query: str) -> Dict[str, Any]:
    """
    Search documentation in a doc2mcp project.
    
    This function simulates querying a project's MCP endpoint to search
    through the uploaded and processed documentation.
    
    Args:
        project_slug: The project slug (generated during upload)
        query: The search query string
        
    Returns:
        A dictionary containing search results with chunks of relevant content
        
    Example:
        >>> results = search("my-project", "authentication")
        >>> print(results["chunks"][0]["content"])
        This is a simulated result for your query.
    """
    # Check if project exists
    if project_slug not in _uploaded_projects:
        print(f"[doc2mcp] Warning: Project '{project_slug}' not found in uploaded projects")
    
    # Simulate search process
    print(f"[doc2mcp] Searching project '{project_slug}' for: {query}")
    print(f"[doc2mcp] Querying embeddings...")
    print(f"[doc2mcp] Ranking results...")
    
    # Generate fake search response
    response = {
        "chunks": [
            {
                "id": "chunk_001",
                "content": f"This is a simulated result for your query: '{query}'. "
                          f"In a real implementation, this would contain relevant "
                          f"documentation content from the {project_slug} project.",
                "metadata": {
                    "source": "index.md",
                    "position": 1,
                    "score": 0.95
                }
            },
            {
                "id": "chunk_002", 
                "content": f"Another simulated chunk related to '{query}'. "
                          f"This demonstrates multiple search results being returned "
                          f"from the documentation corpus.",
                "metadata": {
                    "source": "getting-started.md",
                    "position": 3,
                    "score": 0.87
                }
            },
            {
                "id": "chunk_003",
                "content": f"A third example chunk for '{query}'. "
                          f"Real results would be based on semantic similarity "
                          f"to your query using vector embeddings.",
                "metadata": {
                    "source": "api-reference.md", 
                    "position": 1,
                    "score": 0.82
                }
            }
        ]
    }
    
    print(f"[doc2mcp] Found {len(response['chunks'])} relevant chunks")
    
    return response


def list_projects() -> List[str]:
    """
    List all uploaded projects.
    
    Returns:
        A list of project slugs that have been uploaded in this session
        
    Example:
        >>> projects = list_projects()
        >>> print(projects)
        ['my-project', 'another-project']
    """
    return _uploaded_projects.copy()


if __name__ == "__main__":
    print("=== doc2mcp SDK Demo ===\n")
    
    # Example 1: Upload documentation
    print("1. Uploading documentation...")
    endpoint1 = upload("/path/to/my/docs", "My Awesome Project")
    print(f"   Endpoint: {endpoint1}\n")
    
    # Example 2: Upload another project
    print("2. Uploading another project...")
    endpoint2 = upload("/another/path", "API Documentation")
    print(f"   Endpoint: {endpoint2}\n")
    
    # Example 3: List uploaded projects
    print("3. Listing uploaded projects...")
    projects = list_projects()
    print(f"   Projects: {projects}\n")
    
    # Example 4: Search the first project
    print("4. Searching first project...")
    results1 = search("my-awesome-project", "authentication")
    print(f"   Found {len(results1['chunks'])} results")
    print(f"   First result: {results1['chunks'][0]['content'][:100]}...\n")
    
    # Example 5: Search the second project
    print("5. Searching second project...")
    results2 = search("api-documentation", "endpoints")
    print(f"   Found {len(results2['chunks'])} results")
    print(f"   First result: {results2['chunks'][0]['content'][:100]}...\n")
    
    # Example 6: Search non-existent project
    print("6. Searching non-existent project...")
    results3 = search("non-existent", "test query")
    print(f"   Found {len(results3['chunks'])} results anyway (simulated)\n")
    
    print("=== Demo Complete ===")
"""
Command-line interface for doc2mcp
"""

import argparse
import sys
from pathlib import Path
from typing import List

from .client import Doc2MCPClient
from .exceptions import Doc2MCPError
from .auth import login, logout, whoami, get_authenticated_client


def login_command(args):
    """Handle the login command"""
    try:
        login(args.server, args.api_key)
        return 0
    except Exception as e:
        print(f"Login failed: {e}")
        return 1


def logout_command(args):
    """Handle the logout command"""
    logout()
    return 0


def whoami_command(args):
    """Handle the whoami command"""
    whoami()
    return 0


def upload_command(args):
    """Handle the upload command"""
    try:
        # Use authenticated client
        client = get_authenticated_client(args.server)
        # Collect files from the directory or individual files
        files = []
        if args.directory:
            directory = Path(args.directory)
            if not directory.exists():
                print(f"Error: Directory '{args.directory}' not found")
                return 1
            
            # Find supported file types
            supported_extensions = {'.md', '.markdown', '.html', '.htm', '.txt'}
            for ext in supported_extensions:
                files.extend(directory.glob(f"**/*{ext}"))
        
        if args.files:
            for file_path in args.files:
                files.append(Path(file_path))
        
        if not files:
            print("Error: No files found to upload")
            return 1
        
        print(f"Uploading {len(files)} files...")
        
        project = client.upload_documents(
            name=args.name,
            files=[str(f) for f in files],
            description=args.description or ""
        )
        
        print(f"✓ Project created: {project.name}")
        print(f"  ID: {project.id}")
        print(f"  Slug: {project.slug}")
        print(f"  Status: {project.status.value}")
        print(f"  MCP Endpoint: {client.base_url}{project.mcp_endpoint}")
        print(f"  Files processed: {project.file_count}")
        
        return 0
        
    except Doc2MCPError as e:
        print(f"Error: {e}")
        return 1


def list_command(args):
    """Handle the list command"""
    try:
        # Use authenticated client
        client = get_authenticated_client(args.server)
        projects = client.get_projects()
        
        if not projects:
            print("No projects found")
            return 0
        
        print(f"Found {len(projects)} projects:")
        print()
        
        for project in projects:
            print(f"  {project.name} (ID: {project.id})")
            print(f"    Slug: {project.slug}")
            print(f"    Status: {project.status.value}")
            print(f"    Files: {project.file_count}")
            print(f"    Created: {project.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Endpoint: {client.base_url}{project.mcp_endpoint}")
            if project.description:
                print(f"    Description: {project.description}")
            print()
        
        return 0
        
    except Doc2MCPError as e:
        print(f"Error: {e}")
        return 1


def search_command(args):
    """Handle the search command"""
    try:
        # Use authenticated client
        client = get_authenticated_client(args.server)
        
        # First get the project to retrieve its API token
        projects = client.get_projects()
        project = None
        
        # Find project by slug or name
        for p in projects:
            if p.slug == args.project or p.name == args.project:
                project = p
                break
        
        if not project:
            print(f"Project '{args.project}' not found")
            return 1
        
        # Use the project's API token for search
        results = client.search(project.slug, args.query, project.api_token, args.limit)
        
        if not results.chunks:
            print("No results found")
            return 0
        
        print(f"Found {len(results.chunks)} results:")
        print()
        
        for i, chunk in enumerate(results.chunks, 1):
            print(f"Result {i}:")
            print(f"  Source: {chunk.metadata.get('source', 'Unknown')}")
            print(f"  Type: {chunk.metadata.get('type', 'Unknown')}")
            print(f"  Content: {chunk.content[:200]}...")
            print()
        
        return 0
        
    except Doc2MCPError as e:
        print(f"Error: {e}")
        return 1


def delete_command(args):
    """Handle the delete command"""
    try:
        # Use authenticated client
        client = get_authenticated_client(args.server)
        
        if client.delete_project(args.project_id):
            print(f"✓ Project {args.project_id} deleted successfully")
        return 0
        
    except Doc2MCPError as e:
        print(f"Error: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="doc2mcp - Convert documentation to MCP endpoints"
    )
    parser.add_argument(
        "--server", 
        default="http://localhost:5000",
        help="doc2mcp server URL (default: http://localhost:5000)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Authentication commands
    login_parser = subparsers.add_parser("login", help="Log in to doc2mcp server")
    login_parser.add_argument("--api-key", help="API key (will prompt if not provided)")
    login_parser.set_defaults(func=login_command)
    
    logout_parser = subparsers.add_parser("logout", help="Log out from doc2mcp server")
    logout_parser.set_defaults(func=logout_command)
    
    whoami_parser = subparsers.add_parser("whoami", help="Show current login status")
    whoami_parser.set_defaults(func=whoami_command)
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload documentation files")
    upload_parser.add_argument("name", help="Project name")
    upload_parser.add_argument("--description", help="Project description")
    upload_parser.add_argument("--directory", "-d", help="Directory containing documentation files")
    upload_parser.add_argument("--files", "-f", nargs="+", help="Individual files to upload")
    upload_parser.set_defaults(func=upload_command)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List all projects")
    list_parser.set_defaults(func=list_command)
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search within a project")
    search_parser.add_argument("project", help="Project slug")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=10, help="Maximum results (default: 10)")
    search_parser.set_defaults(func=search_command)
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a project")
    delete_parser.add_argument("project_id", type=int, help="Project ID to delete")
    delete_parser.set_defaults(func=delete_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
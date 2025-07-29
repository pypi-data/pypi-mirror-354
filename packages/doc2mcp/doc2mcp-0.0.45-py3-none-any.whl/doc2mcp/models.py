"""
Data models for the doc2mcp SDK
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional


class ProjectStatus(Enum):
    """Status of a doc2mcp project"""
    PROCESSING = "processing"
    READY = "ready"
    ERROR = "error"


@dataclass
class Project:
    """Represents a doc2mcp project"""
    id: int
    name: str
    slug: str
    description: str
    file_count: int
    status: ProjectStatus
    created_at: datetime
    mcp_endpoint: str
    api_token: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        """Create a Project from API response data"""
        return cls(
            id=data['id'],
            name=data['name'],
            slug=data['slug'],
            description=data['description'],
            file_count=data['fileCount'],
            status=ProjectStatus(data['status']),
            created_at=datetime.fromisoformat(data['createdAt'].replace('Z', '+00:00')),
            mcp_endpoint=data['mcpEndpoint'],
            api_token=data['apiToken']
        )


@dataclass
class DocumentChunk:
    """Represents a processed document chunk"""
    id: str
    content: str
    metadata: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DocumentChunk':
        """Create a DocumentChunk from API response data"""
        return cls(
            id=data['id'],
            content=data['content'],
            metadata=data['metadata']
        )


@dataclass
class SearchResult:
    """Represents search results from an MCP endpoint"""
    chunks: list[DocumentChunk]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchResult':
        """Create SearchResult from API response data"""
        chunks = [DocumentChunk.from_dict(chunk) for chunk in data['chunks']]
        return cls(chunks=chunks)
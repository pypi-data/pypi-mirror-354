"""
Setup script for doc2mcp Python SDK
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="doc2mcp",
    version="0.0.45",
    author="Yacine Zahidi",
    author_email="yacine.zahidi@gmail.com",
    description="Python SDK for converting documentation into MCP-compliant API endpoints for AI assistants",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ell-hol/doc2mcp-python",
    project_urls={
        "Bug Tracker": "https://github.com/ell-hol/doc2mcp-python/issues",
        "Documentation": "https://github.com/ell-hol/doc2mcp-python",
        "Source Code": "https://github.com/ell-hol/doc2mcp-python",
        "Homepage": "https://github.com/ell-hol/doc2mcp-python",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Documentation",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.900",
        ],
        "cli": [
            "rich>=10.0.0",
            "tabulate>=0.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "doc2mcp=doc2mcp.cli:main",
        ],
    },
    keywords=[
        "documentation", "mcp", "api", "endpoint", "ai", "assistant", 
        "claude", "gpt", "openai", "langchain", "semantic-search", "embeddings"
    ],
    include_package_data=True,
    zip_safe=False,
)
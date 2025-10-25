"""
Setup script para TrackHS MCP Server
Permite instalación como paquete para FastMCP Cloud
"""

from setuptools import find_packages, setup

setup(
    name="trackhs-mcp",
    version="2.0.0",
    description="TrackHS MCP Server - Servidor MCP para TrackHS API",
    author="IHSolutions",
    author_email="ihsolutionsco@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastmcp>=2.13.0",
        "httpx>=0.27.0",
        "python-dotenv>=1.0.1",
        "pydantic>=2.12.3",
    ],
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)

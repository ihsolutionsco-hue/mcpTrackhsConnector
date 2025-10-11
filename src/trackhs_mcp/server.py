"""
FastMCP Cloud entrypoint for TrackHS MCP Connector
This file is required by FastMCP Cloud deployment
"""

from dotenv import load_dotenv
from fastmcp import FastMCP

from .infrastructure.adapters.config import TrackHSConfig
from .infrastructure.adapters.trackhs_api_client import TrackHSApiClient
from .infrastructure.mcp.server import register_all_components

# Load environment variables
load_dotenv()

# Create dependencies
config = TrackHSConfig.from_env()
api_client = TrackHSApiClient(config)

# Create MCP server instance (required by FastMCP Cloud)
mcp = FastMCP("TrackHS MCP Server")

# Register all components
register_all_components(mcp, api_client)

# FastMCP Cloud expects the mcp instance to be available at module level
# The server will be started automatically by FastMCP Cloud

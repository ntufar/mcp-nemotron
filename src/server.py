import asyncio
import logging
from typing import Any, Dict
from mcp import Server
from .services.filesystem_service import FileSystemService
from .lib.config import config

# Configure logging
logging.basicConfig(level=getattr(logging, config.log_level))
logger = logging.getLogger(__name__)

# Initialize service with config
fs_service = FileSystemService(
    allowed_paths=config.allowed_paths,
    restricted_paths=config.restricted_paths,
    max_file_size=config.max_file_size
)

# Create MCP server
server = Server("mcp-nemotron")

@server.tool()
async def list_directory(path: str, include_hidden: bool = False, max_depth: int = 0) -> Dict[str, Any]:
    """List contents of a directory with metadata"""
    logger.info(f"Request: list_directory path={path}, include_hidden={include_hidden}, max_depth={max_depth}")
    try:
        result = fs_service.list_directory(path, include_hidden, max_depth)
        logger.info(f"Response: list_directory for {path} returned {len(result.get('items', []))} items")
        return result
    except Exception as e:
        logger.error(f"Error listing directory {path}: {e}")
        return {
            "error": {
                "code": "LIST_ERROR",
                "message": str(e),
                "path": path
            }
        }

@server.tool()
async def read_file(path: str, encoding: str = "auto", start_line: int = None, end_line: int = None) -> Dict[str, Any]:
    """Read content of a file"""
    logger.info(f"Request: read_file path={path}, encoding={encoding}, start_line={start_line}, end_line={end_line}")
    try:
        result = fs_service.read_file(path, encoding, start_line, end_line)
        content_length = len(result.get("content", ""))
        logger.info(f"Response: read_file for {path} returned {content_length} characters")
        return result
    except Exception as e:
        logger.error(f"Error reading file {path}: {e}")
        return {
            "error": {
                "code": "READ_ERROR",
                "message": str(e),
                "path": path
            }
        }

# For testing purposes, add a method to call tools
async def call_tool(tool_name: str, arguments: Dict[str, Any]) -> Any:
    """Helper method to call tools programmatically for testing"""
    if tool_name == "list_directory":
        return await list_directory(**arguments)
    elif tool_name == "read_file":
        return await read_file(**arguments)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

# Add to server for testing
server.call_tool = call_tool
import pytest
import json
import jsonschema
from pathlib import Path

# Load contract schemas
contracts_dir = Path("specs/001-feature-project-to-create-mcp-server-to-help-llm-to-browse/contracts")
list_directory_schema = json.loads((contracts_dir / "list_directory.json").read_text())
list_directory_response_schema = json.loads((contracts_dir / "list_directory_response.json").read_text())

def test_list_directory_request_schema_is_valid():
    """Test that the list_directory request schema is a valid JSON schema"""
    jsonschema.Draft202012Validator.check_schema(list_directory_schema)

def test_list_directory_response_schema_is_valid():
    """Test that the list_directory response schema is a valid JSON schema"""
    jsonschema.Draft202012Validator.check_schema(list_directory_response_schema)

def test_list_directory_tool_exists():
    """Test that the list_directory tool is registered in the MCP server"""
    from src.server import server  # This will fail until server is implemented

    tools = server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "list_directory" in tool_names

def test_list_directory_tool_input_schema():
    """Test that the list_directory tool has the correct input schema"""
    from src.server import server

    tool = next(tool for tool in server.list_tools() if tool.name == "list_directory")
    assert tool.input_schema == list_directory_schema
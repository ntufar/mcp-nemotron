import pytest
import json
import jsonschema
from pathlib import Path

# Load contract schemas
contracts_dir = Path("specs/001-feature-project-to-create-mcp-server-to-help-llm-to-browse/contracts")
read_file_schema = json.loads((contracts_dir / "read_file.json").read_text())
read_file_response_schema = json.loads((contracts_dir / "read_file_response.json").read_text())

def test_read_file_request_schema_is_valid():
    """Test that the read_file request schema is a valid JSON schema"""
    jsonschema.Draft202012Validator.check_schema(read_file_schema)

def test_read_file_response_schema_is_valid():
    """Test that the read_file response schema is a valid JSON schema"""
    jsonschema.Draft202012Validator.check_schema(read_file_response_schema)

def test_read_file_tool_exists():
    """Test that the read_file tool is registered in the MCP server"""
    from src.server import server  # This will fail until server is implemented

    tools = server.list_tools()
    tool_names = [tool.name for tool in tools]
    assert "read_file" in tool_names

def test_read_file_tool_input_schema():
    """Test that the read_file tool has the correct input schema"""
    from src.server import server

    tool = next(tool for tool in server.list_tools() if tool.name == "read_file")
    assert tool.input_schema == read_file_schema
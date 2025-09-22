import pytest
import json
from pathlib import Path

# Load expected response schema
contracts_dir = Path("specs/001-feature-project-to-create-mcp-server-to-help-llm-to-browse/contracts")
response_schema = json.loads((contracts_dir / "list_directory_response.json").read_text())

@pytest.mark.asyncio
async def test_directory_listing_scenario():
    """Test the directory listing scenario from quickstart"""
    from src.server import server  # This will fail until server is implemented

    # Request from quickstart scenario 1
    request = {
        "tool": "list_directory",
        "arguments": {
            "path": "/Users/yourname/projects",
            "include_hidden": False,
            "max_depth": 1
        }
    }

    # Call the tool
    response = await server.call_tool(request["tool"], request["arguments"])

    # Validate response structure matches schema
    # For now, basic checks
    assert isinstance(response, dict)
    assert "directory" in response
    assert "items" in response
    assert isinstance(response["items"], list)

    # Check directory structure
    directory = response["directory"]
    assert "path" in directory
    assert "name" in directory
    assert "permissions" in directory
    assert "modified_time" in directory
    assert "item_count" in directory

    # Check items are either directories or files
    for item in response["items"]:
        assert "type" in item
        assert item["type"] in ["directory", "file"]
        assert "path" in item
        assert "name" in item
        assert "permissions" in item
        assert "modified_time" in item
        if item["type"] == "file":
            assert "size" in item
        else:
            assert "item_count" in item
import pytest
import json
from pathlib import Path

@pytest.mark.asyncio
async def test_access_denied_scenario():
    """Test the access denied scenario from quickstart"""
    from src.server import server  # This will fail until server is implemented

    # Request from quickstart scenario 3
    request = {
        "tool": "list_directory",
        "arguments": {
            "path": "/System"
        }
    }

    # Call the tool - should raise or return error
    with pytest.raises(Exception) as exc_info:
        await server.call_tool(request["tool"], request["arguments"])

    # Or if it returns error response
    # response = await server.call_tool(request["tool"], request["arguments"])
    # assert "error" in response
    # assert response["error"]["code"] == "ACCESS_DENIED"

    # For now, assume it raises
    assert "ACCESS_DENIED" in str(exc_info.value) or "access" in str(exc_info.value).lower()
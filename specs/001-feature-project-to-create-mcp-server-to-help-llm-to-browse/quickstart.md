# Quickstart: MCP Server for LLM Directory and File Browsing

**Date**: 2025-09-21
**Test Environment**: Local development setup

## Prerequisites
- Python 3.11+
- MCP-compatible LLM client (Claude, GPT-4, etc.)
- Access to local file system

## Installation
```bash
pip install mcp-server-filesystem
```

## Configuration
Create a configuration file `config.yaml`:
```yaml
server:
  host: localhost
  port: 3000
  allowed_paths:
    - "/Users/yourname/projects"
    - "/tmp"
  restricted_paths:
    - "/System"
    - "/usr"
    - "/etc"
  max_file_size: 10485760  # 10MB
```

## Starting the Server
```bash
mcp-server-filesystem --config config.yaml
```

## Testing Scenarios

### Scenario 1: Directory Listing
**Given** the MCP server is running and configured
**When** an LLM requests directory listing for `/Users/yourname/projects`
**Then** the server returns a list of files and subdirectories

**MCP Tool Call**:
```json
{
  "tool": "list_directory",
  "arguments": {
    "path": "/Users/yourname/projects",
    "include_hidden": false,
    "max_depth": 1
  }
}
```

**Expected Response**:
```json
{
  "directory": {
    "path": "/Users/yourname/projects",
    "name": "projects",
    "permissions": {"readable": true, "writable": true, "executable": true},
    "modified_time": "2025-09-21T10:00:00Z",
    "item_count": 5
  },
  "items": [
    {
      "type": "directory",
      "path": "/Users/yourname/projects/mcp-nemotron",
      "name": "mcp-nemotron",
      "permissions": {"readable": true, "writable": true, "executable": true},
      "modified_time": "2025-09-21T09:30:00Z",
      "item_count": 12
    },
    {
      "type": "file",
      "path": "/Users/yourname/projects/README.md",
      "name": "README.md",
      "size": 1024,
      "permissions": {"readable": true, "writable": true, "executable": false},
      "modified_time": "2025-09-20T15:45:00Z",
      "mime_type": "text/markdown"
    }
  ]
}
```

### Scenario 2: File Reading
**Given** the MCP server is running
**When** an LLM requests to read `/Users/yourname/projects/README.md`
**Then** the server returns the file content

**MCP Tool Call**:
```json
{
  "tool": "read_file",
  "arguments": {
    "path": "/Users/yourname/projects/README.md",
    "encoding": "utf-8"
  }
}
```

**Expected Response**:
```json
{
  "file": {
    "path": "/Users/yourname/projects/README.md",
    "name": "README.md",
    "size": 1024,
    "mime_type": "text/markdown",
    "encoding": "utf-8",
    "permissions": {"readable": true, "writable": true, "executable": false},
    "modified_time": "2025-09-20T15:45:00Z"
  },
  "content": "# My Projects\n\nThis directory contains my development projects...\n",
  "lines": 25,
  "truncated": false
}
```

### Scenario 3: Access Denied
**Given** the MCP server is running with restricted paths
**When** an LLM requests access to `/System`
**Then** the server denies access with an error

**MCP Tool Call**:
```json
{
  "tool": "list_directory",
  "arguments": {
    "path": "/System"
  }
}
```

**Expected Response**:
```json
{
  "error": {
    "code": "ACCESS_DENIED",
    "message": "Access to path '/System' is restricted",
    "path": "/System"
  }
}
```

## Integration Examples

### Claude Code Integration
```python
import anthropic
from mcp import Client

# Initialize MCP client
mcp_client = Client(server_url="http://localhost:3000")

# Use with Claude
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=1000,
    system="You have access to file system tools.",
    messages=[{
        "role": "user",
        "content": "List the contents of my projects directory"
    }],
    tools=mcp_client.get_tools()
)
```

### OpenAI GPT Integration
```python
import openai
from mcp import Client

# Initialize MCP client
mcp_client = Client(server_url="http://localhost:3000")

# Use with GPT-4
client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{
        "role": "user",
        "content": "Read the README file in my projects directory"
    }],
    tools=mcp_client.get_tools(),
    tool_choice="auto"
)
```

## Troubleshooting

### Common Issues
1. **Permission Denied**: Ensure the server has read access to requested paths
2. **File Too Large**: Increase `max_file_size` in configuration
3. **Connection Failed**: Verify server is running on correct host/port
4. **Encoding Errors**: Try different encoding or check file type

### Logs
Server logs are written to `server.log` with detailed error information.

## Performance Benchmarks
- Directory listing (< 100ms for 100 items)
- File reading (< 1s for 10MB files)
- Concurrent requests (up to 10 simultaneous)
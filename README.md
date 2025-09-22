# MCP Server for LLM Directory and File Browsing

An MCP (Model Context Protocol) server that provides secure API endpoints for LLMs to browse local directories and read files.

## Features

- **Secure Directory Listing**: List directory contents with metadata
- **Safe File Reading**: Read file contents with configurable encoding
- **Access Control**: Configurable allowed/restricted paths
- **Performance Optimized**: Fast responses for LLM consumption
- **Cross-platform**: Works on Linux, macOS, and Windows

## Installation

```bash
pip install mcp-nemotron
```

Or from source:

```bash
git clone <repository>
cd mcp-nemotron
pip install -e .
```

## Configuration

Set environment variables:

```bash
export ALLOWED_PATHS="/Users,/tmp"
export RESTRICTED_PATHS="/System,/usr,/etc"
export MAX_FILE_SIZE="10485760"  # 10MB
export HOST="localhost"
export PORT="3000"
export LOG_LEVEL="INFO"
```

## Usage

### Starting the Server

```bash
python -m src.server
```

### With LLM Integration

The server provides two main tools:

#### list_directory
Lists contents of a directory with metadata.

**Parameters:**
- `path`: Absolute path to directory
- `include_hidden`: Include hidden files (default: false)
- `max_depth`: Recursion depth (default: 0)

#### read_file
Reads content of a file.

**Parameters:**
- `path`: Absolute path to file
- `encoding`: Text encoding (default: auto)
- `start_line`: Starting line number
- `end_line`: Ending line number

### Example Usage

```python
import asyncio
from src.server import server

async def main():
    # List directory
    result = await server.call_tool("list_directory", {"path": "/tmp"})
    print(result)

    # Read file
    result = await server.call_tool("read_file", {"path": "/tmp/example.txt"})
    print(result["content"])

asyncio.run(main())
```

## Security

- Paths are validated and normalized
- Access is restricted to configured allowed paths
- System directories are blocked by default
- File size limits prevent memory exhaustion
- All operations are logged

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
black src/
flake8 src/
```

## License

MIT License
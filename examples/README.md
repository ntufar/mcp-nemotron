# MCP Server Integration Examples

This directory contains examples showing how to integrate the MCP filesystem server with various LLM APIs.

## Available Examples

### Gemini API (`gemini_example.py`)
Demonstrates integration with Google's Gemini API using function calling.

**Setup:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
pip install google-generativeai
```

**Run:**
```bash
# Terminal 1: Start MCP server
python -m src.server

# Terminal 2: Run example
python examples/gemini_example.py
```

### Claude API (`claude_example.py`)
Integration with Anthropic's Claude API.

### OpenAI API (`openai_example.py`)
Integration with OpenAI's GPT models.

## Prerequisites

- MCP server running on `http://localhost:3000`
- Appropriate API keys set as environment variables
- Required Python packages installed

## Security Note

These examples demonstrate secure file access through the MCP server. The server enforces:
- Path validation and normalization
- Configurable access restrictions
- File size limits
- Audit logging

Make sure to configure `ALLOWED_PATHS` and `RESTRICTED_PATHS` appropriately for your use case.
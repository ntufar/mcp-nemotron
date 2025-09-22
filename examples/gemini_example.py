#!/usr/bin/env python3
"""
Example: Using MCP Server with Google Gemini API

This example demonstrates how to integrate the MCP filesystem server
with Google's Gemini API for secure file system access.

Prerequisites:
- pip install google-generativeai mcp-server-filesystem
- Set GOOGLE_API_KEY environment variable
- Start the MCP server: python -m src.server
"""

import os
import asyncio
import google.generativeai as genai
from mcp import Client

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize MCP client for filesystem server
mcp_client = Client(server_url="http://localhost:3000")

async def main():
    """Main example function"""
    print("🤖 Gemini + MCP Filesystem Integration Example")
    print("=" * 50)

    # Initialize Gemini model with tools
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        tools=mcp_client.get_tools()
    )

    # Example 1: List directory contents
    print("\n📁 Example 1: Directory Listing")
    prompt1 = "List the contents of the /tmp directory, including file sizes and permissions."

    response1 = model.generate_content(prompt1)
    print(f"Prompt: {prompt1}")
    print(f"Gemini Response: {response1.text}")

    # Example 2: Read a file
    print("\n📄 Example 2: File Reading")
    prompt2 = "Read the contents of /tmp/example.txt if it exists, or explain why it doesn't."

    response2 = model.generate_content(prompt2)
    print(f"Prompt: {prompt2}")
    print(f"Gemini Response: {response2.text}")

    # Example 3: Analyze project structure
    print("\n🔍 Example 3: Project Analysis")
    prompt3 = "Analyze the structure of the mcp-nemotron project directory and summarize what this project does."

    response3 = model.generate_content(prompt3)
    print(f"Prompt: {prompt3}")
    print(f"Gemini Response: {response3.text}")

    print("\n✅ Examples completed!")

if __name__ == "__main__":
    # Note: In a real implementation, you would run the MCP server separately
    # This example assumes the server is running on localhost:3000
    print("Make sure the MCP server is running:")
    print("python -m src.server")
    print()

    asyncio.run(main())
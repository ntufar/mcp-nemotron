#!/bin/bash
# Parse arguments
if [ "$1" != "--json" ]; then
    echo "Usage: $0 --json \"feature description\""
    exit 1
fi
JSON_INPUT="$2"

# Generate branch name from description
BRANCH_NAME="feature-$(echo "$JSON_INPUT" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9 ]//g' | tr ' ' '-' | cut -c1-50)"

# Absolute path for spec file
SPEC_FILE="$(pwd)/.specify/specs/${BRANCH_NAME}.md"

# Create directory if needed
mkdir -p "$(dirname "$SPEC_FILE")"

# Initialize spec file with basic structure
cat > "$SPEC_FILE" <<EOL
# MCP Server Feature Specification

## Feature Description
$JSON_INPUT

## Technical Requirements
- Directory traversal support
- File content reading/writing
- LLM interaction protocol

## Implementation Plan
1. Implement MCP server endpoint
2. Develop file browser UI
3. Integrate LLM navigation logic
EOL

# Create and checkout new branch
git checkout -b "$BRANCH_NAME"
git add "$SPEC_FILE"

# Output JSON
echo "{\"BRANCH_NAME\": \"$BRANCH_NAME\", \"SPEC_FILE\": \"$SPEC_FILE\"}"
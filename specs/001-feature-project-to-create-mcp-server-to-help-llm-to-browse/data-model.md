# Data Model: MCP Server for LLM Directory and File Browsing

**Date**: 2025-09-21
**Based on**: spec.md requirements

## Entities

### Directory
Represents a file system directory with navigation and listing capabilities.

**Fields**:
- `path`: str (absolute path, required)
- `name`: str (directory name, required)
- `parent_path`: str (parent directory path, optional)
- `children`: List[Union[Directory, File]] (child items, lazy-loaded)
- `permissions`: dict (read/write/execute permissions, required)
- `modified_time`: datetime (last modification time, required)
- `created_time`: datetime (creation time, optional)

**Validation Rules**:
- Path must be absolute and normalized
- Path must exist and be a directory
- User must have read permission
- Path must not be in restricted directories (system, hidden, etc.)

**Relationships**:
- Parent: Directory (self-referencing)
- Children: Directory | File (polymorphic)

### File
Represents a file in the file system with content access.

**Fields**:
- `path`: str (absolute path, required)
- `name`: str (file name, required)
- `extension`: str (file extension, optional)
- `size`: int (file size in bytes, required)
- `mime_type`: str (MIME type, optional)
- `encoding`: str (text encoding if applicable, optional)
- `permissions`: dict (read/write permissions, required)
- `modified_time`: datetime (last modification time, required)
- `created_time`: datetime (creation time, optional)
- `content`: bytes | str (file content, lazy-loaded)

**Validation Rules**:
- Path must be absolute and normalized
- Path must exist and be a file
- User must have read permission
- File size must be within configured limits
- Path must not be in restricted locations

**Relationships**:
- Parent: Directory (containing directory)

## Data Flow

### Directory Listing
1. Validate path access permissions
2. Read directory contents
3. Filter restricted items
4. Create Directory/File entities
5. Return paginated results

### File Reading
1. Validate file access permissions
2. Check file size limits
3. Read content with appropriate encoding
4. Return content with metadata

## State Transitions

### Directory States
- `accessible`: Can be listed
- `restricted`: Access denied
- `not_found`: Directory doesn't exist

### File States
- `readable`: Can be read
- `too_large`: Exceeds size limit
- `restricted`: Access denied
- `not_found`: File doesn't exist
- `encoding_error`: Cannot decode content

## Validation Constraints

- Maximum directory depth: Unlimited (but track for performance)
- Maximum file size: Configurable (default 10MB)
- Restricted paths: System directories, hidden files, user-configured exclusions
- Encoding detection: Automatic for text files, binary for others
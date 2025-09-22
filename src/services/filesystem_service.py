import os
import pathlib
import mimetypes
import logging
from typing import List, Union, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
from ..models.directory import Directory
from ..models.file import File

logger = logging.getLogger(__name__)

class FileSystemService:
    def __init__(self, allowed_paths: Optional[List[str]] = None, restricted_paths: Optional[List[str]] = None, max_file_size: int = 10 * 1024 * 1024):
        self.allowed_paths = [Path(p).resolve() for p in (allowed_paths or [])]
        self.restricted_paths = [Path(p).resolve() for p in (restricted_paths or ["/System", "/usr", "/etc"])]
        self.max_file_size = max_file_size

    def _is_path_allowed(self, path: Path) -> bool:
        """Check if path is allowed based on whitelist/blacklist"""
        resolved = path.resolve()

        # Check restricted paths
        for restricted in self.restricted_paths:
            if resolved.is_relative_to(restricted):
                return False

        # If whitelist is set, check against it
        if self.allowed_paths:
            return any(resolved.is_relative_to(allowed) for allowed in self.allowed_paths)

        # No whitelist, allow all except restricted
        return True

    def _get_permissions(self, path: Path) -> Dict[str, bool]:
        """Get file/directory permissions"""
        return {
            "readable": os.access(path, os.R_OK),
            "writable": os.access(path, os.W_OK),
            "executable": os.access(path, os.X_OK)
        }

    def list_directory(self, path: str, include_hidden: bool = False, max_depth: int = 0) -> Dict[str, Any]:
        """List directory contents"""
        dir_path = Path(path).resolve()

        if not dir_path.exists() or not dir_path.is_dir():
            raise ValueError(f"Directory does not exist: {path}")

        if not self._is_path_allowed(dir_path):
            raise PermissionError(f"Access denied to: {path}")

        permissions = self._get_permissions(dir_path)
        if not permissions["readable"]:
            raise PermissionError(f"No read permission for: {path}")

        # Get directory info
        stat = dir_path.stat()
        directory = Directory(
            path=str(dir_path),
            name=dir_path.name,
            permissions=permissions,
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            created_time=datetime.fromtimestamp(stat.st_ctime)
        )

        items = []
        try:
            for item_path in dir_path.iterdir():
                if not include_hidden and item_path.name.startswith('.'):
                    continue

                if not self._is_path_allowed(item_path):
                    continue

                stat = item_path.stat()
                permissions = self._get_permissions(item_path)

                if item_path.is_dir():
                    item = Directory(
                        path=str(item_path),
                        name=item_path.name,
                        permissions=permissions,
                        modified_time=datetime.fromtimestamp(stat.st_mtime),
                        created_time=datetime.fromtimestamp(stat.st_ctime)
                    )
                else:
                    mime_type, _ = mimetypes.guess_type(str(item_path))
                    item = File(
                        path=str(item_path),
                        name=item_path.name,
                        size=stat.st_size,
                        mime_type=mime_type,
                        permissions=permissions,
                        modified_time=datetime.fromtimestamp(stat.st_mtime),
                        created_time=datetime.fromtimestamp(stat.st_ctime)
                    )

                items.append(item)

        except PermissionError:
            logger.warning(f"Permission denied accessing directory: {path}")

        return {
            "directory": directory.to_dict(),
            "items": [item.to_dict() for item in items]
        }

    def read_file(self, path: str, encoding: str = "auto", start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
        """Read file content"""
        file_path = Path(path).resolve()

        if not file_path.exists() or not file_path.is_file():
            raise ValueError(f"File does not exist: {path}")

        if not self._is_path_allowed(file_path):
            raise PermissionError(f"Access denied to: {path}")

        permissions = self._get_permissions(file_path)
        if not permissions["readable"]:
            raise PermissionError(f"No read permission for: {path}")

        stat = file_path.stat()
        if stat.st_size > self.max_file_size:
            raise ValueError(f"File too large: {stat.st_size} bytes > {self.max_file_size}")

        mime_type, _ = mimetypes.guess_type(str(file_path))

        # Determine encoding
        if encoding == "auto":
            encoding = "utf-8" if mime_type and mime_type.startswith("text/") else None

        # Read content
        try:
            if encoding:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                lines = content.count('\n') + 1
            else:
                with open(file_path, 'rb') as f:
                    content = f.read()
                lines = None
        except UnicodeDecodeError:
            raise ValueError(f"Cannot decode file with encoding: {encoding}")

        file_obj = File(
            path=str(file_path),
            name=file_path.name,
            size=stat.st_size,
            mime_type=mime_type,
            encoding=encoding,
            permissions=permissions,
            modified_time=datetime.fromtimestamp(stat.st_mtime),
            created_time=datetime.fromtimestamp(stat.st_ctime),
            content=content
        )

        return {
            "file": {
                "path": file_obj.path,
                "name": file_obj.name,
                "size": file_obj.size,
                "mime_type": file_obj.mime_type,
                "encoding": file_obj.encoding,
                "permissions": file_obj.permissions,
                "modified_time": file_obj.modified_time.isoformat()
            },
            "content": content,
            "lines": lines,
            "truncated": False
        }
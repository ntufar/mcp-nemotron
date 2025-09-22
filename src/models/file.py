from pydantic import BaseModel
from typing import Dict, Optional, Union
from datetime import datetime

class File(BaseModel):
    path: str
    name: str
    extension: Optional[str] = None
    size: int
    mime_type: Optional[str] = None
    encoding: Optional[str] = None
    permissions: Dict[str, bool]
    modified_time: datetime
    created_time: Optional[datetime] = None
    content: Optional[Union[str, bytes]] = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.extension is None and '.' in self.name:
            self.extension = self.name.split('.')[-1]

    def _load_content(self):
        """Load content from filesystem - placeholder for now"""
        # This will be implemented in the service
        pass

    @property
    def is_text(self) -> bool:
        """Check if file is likely text-based"""
        if self.mime_type:
            return self.mime_type.startswith('text/')
        return self.extension in ['txt', 'md', 'py', 'js', 'html', 'css', 'json', 'xml', 'yaml', 'yml']

    def to_dict(self) -> Dict:
        """Convert to dict for API responses"""
        return {
            "path": self.path,
            "name": self.name,
            "size": self.size,
            "permissions": self.permissions,
            "modified_time": self.modified_time.isoformat(),
            "mime_type": self.mime_type,
            "type": "file"
        }
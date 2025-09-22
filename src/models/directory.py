from pydantic import BaseModel
from typing import List, Union, Dict, Optional
from datetime import datetime
from .file import File

class Directory(BaseModel):
    path: str
    name: str
    parent_path: Optional[str] = None
    children: List[Union['Directory', File]] = []
    permissions: Dict[str, bool]
    modified_time: datetime
    created_time: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        # Lazy load children if needed
        if not self.children:
            self._load_children()

    def _load_children(self):
        """Load children from filesystem - placeholder for now"""
        # This will be implemented in the service
        pass

    @property
    def item_count(self) -> int:
        return len(self.children)

    def to_dict(self) -> Dict:
        """Convert to dict for API responses"""
        return {
            "path": self.path,
            "name": self.name,
            "permissions": self.permissions,
            "modified_time": self.modified_time.isoformat(),
            "item_count": self.item_count
        }
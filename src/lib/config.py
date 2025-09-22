import os
from typing import List, Optional
from pathlib import Path

class Config:
    def __init__(self):
        self.allowed_paths: List[str] = self._get_list_env("ALLOWED_PATHS", ["/Users"])
        self.restricted_paths: List[str] = self._get_list_env("RESTRICTED_PATHS", ["/System", "/usr", "/etc"])
        self.max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
        self.host: str = os.getenv("HOST", "localhost")
        self.port: int = int(os.getenv("PORT", "3000"))
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")

    def _get_list_env(self, key: str, default: List[str]) -> List[str]:
        value = os.getenv(key)
        if value:
            return [p.strip() for p in value.split(",")]
        return default

config = Config()
# Stub file for ntfy_logging.__init__

from typing import Optional, Dict
import logging

class NtfyHandler(logging.Handler):
    DEFAULT_PRIORITY: int
    LOG_LEVEL_PRIORITY_MAP: Dict[int, int]
    PRIORITY_TAGS_MAP: Dict[int, str]

    def __init__(
        self,
        topic_name: str,
        server_url: str = ..., 
        access_token: Optional[str] = ..., 
        username: Optional[str] = ..., 
        password: Optional[str] = ..., 
        priority_tags_map: Optional[Dict[int, str]] = ..., 
        log_level_priority_map: Optional[Dict[int, int]] = ..., 
        click: Optional[str] = ..., 
        include_traceback: Optional[bool] = ...,
    ) -> None: ...

    def emit(self, record: logging.LogRecord) -> None: ...
    def close(self) -> None: ...

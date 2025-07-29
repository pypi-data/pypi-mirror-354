"""
Logging handler for ntfy.

This module provides a logging.Handler implementation that sends log 
messages to ntfy, a simple notification service.
"""
import logging
from ntfy_api import NtfyClient, Credentials, Message
from typing import Optional, Dict
from .types import *



class NtfyHandler(logging.Handler):
    """
    A logging handler that sends logs to ntfy using ntfy_api.
    
    This handler formats logs according to the specified format and sends
    them to the specified ntfy topic. It supports customization of the
    notification priority based on the log level.
    """

    DEFAULT_PRIORITY: PRIORITY = 3
    LOG_LEVEL_PRIORITY_MAP: Dict[int, PRIORITY] = {
        logging.DEBUG: 1,
        logging.INFO: 2,
        logging.WARNING: 3,
        logging.ERROR: 4,
        logging.FATAL: 5,
    }
    PRIORITY_TAGS_MAP: Dict[int, EMOJI] = {
        1: "incoming_envelope",
        2: "information_source",
        3: "warning",
        4: "exclamation",
        5: "rotating_light",
    }

    def __init__(
        self,
        topic_name: str,
        server_url: str = "https://ntfy.sh",
        access_token: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        priority_tags_map: Optional[Dict[int, EMOJI]] = PRIORITY_TAGS_MAP,
        log_level_priority_map: Optional[Dict[int, PRIORITY]] = LOG_LEVEL_PRIORITY_MAP,
        click: Optional[str] = None,
        include_traceback: Optional[bool] = False,
        markdown: Optional[bool] = False,
    ) -> None:
        """Initialize the NtfyHandler.

        Args:
            topic_name (str): The name of the ntfy topic.
            server_url (str, optional): The URL of the ntfy server. Defaults to "https://ntfy.sh".
            access_token (Optional[str], optional): The access token for ntfy. Defaults to None.
            username (Optional[str], optional): The username for ntfy. Defaults to None.
            password (Optional[str], optional): The password for ntfy. Defaults to None.
            log_level_priority_map (Optional[Dict[int, int]], optional): A mapping of log levels to ntfy priority levels. Defaults to None.
        """
        super().__init__()
        self.topic = topic_name
        self.server_url = server_url
        self.credentials = None
        self.priority_tags_map = priority_tags_map or self.PRIORITY_TAGS_MAP
        self.log_level_priority_map = log_level_priority_map or self.LOG_LEVEL_PRIORITY_MAP
        self.click = click
        self.include_traceback = include_traceback
        self.markdown = markdown

        if access_token:
            self.credentials = Credentials(bearer = access_token)
        elif username and password:
            self.credentials = Credentials(basic = (username, password))

        self.client = NtfyClient(
            base_url = server_url,
            default_topic = topic_name,
            credentials = self.credentials
        )

    def emit(self, record: logging.LogRecord) -> None:
        """Send a log message to ntfy.

        Args:
            record (logging.LogRecord): The log record to send.
        """
        try:
            rounded_level = record.levelno // 10 * 10
            
            priority = self.log_level_priority_map.get(rounded_level, self.DEFAULT_PRIORITY)
            title = f"{record.levelname}: {record.name}"
            message = self.format(record)
            tags: list[EMOJI] = [self.priority_tags_map.get(priority, "warning")]
            
            if self.include_traceback and record.exc_info:
                import traceback
                tb_formatted = traceback.format_exception(*record.exc_info)
                message += '\n\n' + ''.join(tb_formatted)
            
            msg = Message(
                priority = priority,
                title = title,
                message = message,
                tags = tags,
                click = self.click,
                markdown = self.markdown,
            )
            self.client.publish(msg)    #type: ignore

        except Exception:
            self.handleError(record)

    def close(self) -> None:
        """Close the handler and release resources."""
        try:
            if hasattr(self, 'client') and self.client:
                self.client.close()
        except Exception:
            pass
        super().close()

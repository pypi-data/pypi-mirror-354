# ntfy-logging

A Python logging handler for sending logs to [ntfy](https://ntfy.sh/), a simple notification service.

## Installation

### Poetry
```bash
poetry add ntfy-logging
```

### Pip
```bash
pip install ntfy-logging
```

### uv
```bash
uv add ntfy-logging
```

## Basic Usage

```python
import logging
from ntfy_logging import NtfyHandler

# Create logger
logger = logging.getLogger("my_app")
logger.setLevel(logging.DEBUG)

# Create ntfy handler (only send WARNING or higher to ntfy)
ntfy_handler = NtfyHandler(
    topic_name = "your-topic",  # Replace with your ntfy topic
    server_url = "https://ntfy.sh",  # Optional: your ntfy server
    access_token = "your-access-token",  # Optional: for private servers
    include_traceback = True,  # Include exception tracebacks in notifications
)
ntfy_handler.setLevel(logging.WARNING)  # Only WARNING or higher go to ntfy
logger.addHandler(ntfy_handler)

# Log messages
logger.debug("This is a debug message (won't go to ntfy)")
logger.info("This is an info message (won't go to ntfy)")
logger.warning("This is a warning message (will go to ntfy)")
logger.error("This is an error message (will go to ntfy)")
logger.critical("This is a critical message (will go to ntfy)")

# Log exceptions with traceback
try:
    1 / 0
except Exception:
    logger.exception("An error occurred")
```

## Advanced Usage

The `NtfyHandler` class supports many customization options:

```python
import logging
from ntfy_logging import NtfyHandler

# Custom priority mapping
priority_mapping = {
    logging.CRITICAL: 5,  # Max
    logging.ERROR: 4,     # High
    logging.WARNING: 3,   # Default
    logging.INFO: 2,      # Low
    logging.DEBUG: 1,     # Min
}

# Custom tags mapping
tag_mapping = {
    5: "rotating_light",
    4: "exclamation",
    3: "warning",
    2: "information_source",
    1: "incoming_envelope",
}

# Authentication (if your ntfy server requires it)
# For bearer token:
# credentials = ntfy_api.Credentials(bearer="your-auth-token")
# For basic auth:
# credentials = ntfy_api.Credentials(basic=("username", "password"))

logger = logging.getLogger("my_app")

# Create handler with custom configuration
ntfy_handler = NtfyHandler(
    topic_name = "your-topic",
    server_url = "https://ntfy.sh",  # Change if using a self-hosted server
    access_token = "your-access-token",  # Or use credentials=...
    log_level_priority_map = priority_mapping,
    priority_tags_map = tag_mapping,
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
    click = "https://your-app-dashboard.com",  # URL opened when notification is clicked
    include_traceback = True,  # Include exception tracebacks in notifications
)
ntfy_handler.setLevel(logging.WARNING)
logger.addHandler(ntfy_handler)
```

## Features

- Automatic mapping of logging levels to ntfy priorities
- Custom emoji tags for different log levels
- Support for exception logging with tracebacks
- Authentication support for private ntfy servers
- Customizable message formatting
- Support for click actions
- Context manager support for clean resource handling

## CI

This project uses GitHub Actions to run tests with pytest on every push and pull request.

## Credits

This project vendors (bundles) the ntfy-api Python package, licensed under the Apache License 2.0. The ntfy_api source code is included directly in this package; you do not need to install it separately.

Note: ntfy-api is bundled because PyPI does not allow dependencies from git repositories and the PyPI version of ntfy-api is outdated.

- ntfy-api: https://github.com/tanrbobanr/ntfy-api
- Copyright © ntfy-api authors

See the NOTICE file and https://www.apache.org/licenses/LICENSE-2.0 for details.
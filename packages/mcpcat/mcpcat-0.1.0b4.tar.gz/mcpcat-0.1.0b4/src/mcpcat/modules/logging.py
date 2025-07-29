"""Logging functionality for MCPCat."""
import os
from datetime import datetime, timezone
from mcpcat.modules.constants import LOG_PATH


def write_to_log(message: str) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = f"[{timestamp}] {message}\n"

    try:
        # Ensure log directory exists
        log_dir = os.path.dirname(LOG_PATH)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # Write to log file
        with open(LOG_PATH, "a") as f:
            f.write(log_entry)
    except Exception:
        # Silently fail - we don't want logging errors to break the server
        pass

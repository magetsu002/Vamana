"""Logging utilities for workflow execution."""

from datetime import datetime
from engine.config import SYSTEM_LOG, MAX_LOG_MESSAGE_LENGTH


def sanitize_log_message(message: object) -> str:
    """Sanitize a message for logging."""
    message = str(message)

    message = message.replace("\n", "\\n")
    message = message.replace("\r", "\\r")

    if len(message) > MAX_LOG_MESSAGE_LENGTH:
        message = message[:MAX_LOG_MESSAGE_LENGTH] + "...[truncated]"

    return message


def log_system_event(message: str) -> None:
    """Log system events with timestamp to system.log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = sanitize_log_message(message)

    with open(SYSTEM_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

        # Separate runs visually in log file
        if "finished" in message.lower() or "crashed" in message.lower():
            f.write("=" * 120 + "\n\n")

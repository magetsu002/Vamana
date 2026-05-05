"""Step handlers for workflow execution."""

import time

from engine.security import resolve_safe_path, safe_open_write, safe_open_append, safe_open_read
from engine.logging_utils import log_system_event
from engine.validation import PrintStep, WriteFileStep, AppendFileStep, ReadFileStep, WaitStep


def execute_print(step: PrintStep) -> None:
    """Print a message to console."""
    print(step["message"])


def execute_write_file(step: WriteFileStep) -> None:
    """Write content to a file, overwriting if it exists."""
    filename = resolve_safe_path(step["filename"])
    content = step["content"]

    with safe_open_write(filename) as f:
        f.write(content)


def execute_append_file(step: AppendFileStep) -> None:
    """Append content to an existing file."""
    filename = resolve_safe_path(step["filename"])
    content = step["content"]

    with safe_open_append(filename) as f:
        f.write(content)


def execute_read_file(step: ReadFileStep) -> None:
    """Read file content and log the operation."""
    filename = resolve_safe_path(step["filename"])

    with safe_open_read(filename) as f:
        content = f.read()
        log_system_event(f"Read {len(content)} characters from {filename.name}")


def execute_wait(step: WaitStep) -> None:
    """Sleep for specified number of seconds."""
    seconds = step["seconds"]
    time.sleep(seconds)


# Maps step type → function (core engine idea)
STEP_HANDLERS = {
    "print": execute_print,
    "write_file": execute_write_file,
    "append_file": execute_append_file,
    "read_file": execute_read_file,
    "wait": execute_wait,
}

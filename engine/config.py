"""Configuration and constants for the workflow engine."""

from pathlib import Path
from typing import Literal

# Safe workspace directory for file operations
SAFE_DIR = Path("workspace")
SAFE_DIR.mkdir(exist_ok=True)

# Set log path
SYSTEM_LOG = Path("system.log")

# Max limits and constraints
MAX_WAIT_SECONDS = 30
MAX_TOTAL_WAIT_SECONDS = 120
MAX_STEPS = 100
MAX_WORKFLOW_FILE_SIZE = 100 * 1024
MAX_TEXT_FIELD = 10 * 1024
MAX_LOG_MESSAGE_LENGTH = 500

PROTECTED_FILENAMES = {
    "system.log",
    "project.py",
    "test_project.py",
    "schema.sql",
    "database.db",
}

# Defines required fields per step type
STEP_SCHEMAS = {
    "print": {"message": str},
    "write_file": {"filename": str, "content": str},
    "append_file": {"filename": str, "content": str},
    "read_file": {"filename": str},
    "wait": {"seconds": (int, float)},
}

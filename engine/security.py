"""Security utilities for safe file operations and path handling."""

import os
from pathlib import Path

from engine.config import SAFE_DIR, PROTECTED_FILENAMES


def resolve_safe_path(filename: str) -> Path:
    """Resolve file path safely within SAFE_DIR, preventing traversal attacks."""
    if not isinstance(filename, str):
        raise ValueError("File name must be a string")

    path = Path(filename)

    if path.is_absolute():
        raise ValueError("Absolute paths are not allowed")

    if ".." in path.parts:
        raise ValueError("Path traversal is not allowed :<")

    safe_root = SAFE_DIR.resolve()
    target = (SAFE_DIR / path).resolve()

    if not target.is_relative_to(safe_root):
        raise ValueError("Path escapes workspace")

    if path.name in PROTECTED_FILENAMES:
        raise ValueError("Protected file cannot be modified")

    return target


def safe_open_write(path: Path):
    """Safely open file for writing with security flags."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW | os.O_CLOEXEC
    permissions = 0o600

    try:
        fd = os.open(path, flags, permissions)
    except OSError as e:
        raise ValueError(f"Unsafe file operation: {e}")

    return open(fd, "w", encoding="utf-8")


def safe_open_append(path: Path):
    """Safely open file for appending with security flags."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW | os.O_CLOEXEC
    permissions = 0o600

    try:
        fd = os.open(path, flags, permissions)
    except OSError as e:
        raise ValueError(f"Unsafe file operation: {e}")

    return open(fd, "a", encoding="utf-8")


def safe_open_read(path: Path):
    """Safely open file for reading with security flags."""
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC

    try:
        fd = os.open(path, flags)
    except OSError as e:
        raise ValueError(f"Unsafe file operation: {e}")
    return open(fd, "r", encoding="utf-8")

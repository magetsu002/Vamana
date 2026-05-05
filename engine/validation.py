"""Workflow validation and loading."""

import json
from pathlib import Path
from typing import TypedDict, Union, Literal

from engine.config import (
    STEP_SCHEMAS,
    MAX_STEPS,
    MAX_WORKFLOW_FILE_SIZE,
    MAX_TEXT_FIELD,
    MAX_WAIT_SECONDS,
    MAX_TOTAL_WAIT_SECONDS,
)


# TypedDict definitions for type safety
class PrintStep(TypedDict):
    """Print step: outputs a message to console."""
    type: Literal["print"]
    message: str


class WriteFileStep(TypedDict):
    """Write file step: creates or overwrites a file with content."""
    type: Literal["write_file"]
    filename: str
    content: str


class AppendFileStep(TypedDict):
    """Append file step: adds content to the end of a file."""
    type: Literal["append_file"]
    filename: str
    content: str


class ReadFileStep(TypedDict):
    """Read file step: reads and logs file content."""
    type: Literal["read_file"]
    filename: str


class WaitStep(TypedDict):
    """Wait step: pauses execution for a specified duration."""
    type: Literal["wait"]
    seconds: float


# Union type representing any valid step
Step = Union[PrintStep, WriteFileStep, AppendFileStep, ReadFileStep, WaitStep]


class Workflow(TypedDict):
    """Complete workflow definition."""
    name: str
    steps: list[Step]


def load_workflow(filename: str) -> Workflow:
    """Load and parse JSON workflow file."""
    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError("File not found!")

    if path.stat().st_size > MAX_WORKFLOW_FILE_SIZE:
        raise ValueError("Workflow file is too large!")

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("File not found!")

    return data


def validate_workflow(data: Workflow) -> None:
    """Validate top-level workflow structure and all steps."""
    if not isinstance(data, dict):
        raise ValueError("Data needs to be a dictionary")

    if "name" not in data:
        raise ValueError("Data requires a name!")
    if "steps" not in data:
        raise ValueError("Data requires steps!")

    name = data["name"]
    steps = data["steps"]

    if not isinstance(name, str):
        raise ValueError("Name needs to be a string!")
    if not isinstance(steps, list):
        raise ValueError("Steps needs to be a list!")
    if len(steps) > MAX_STEPS:
        raise ValueError(f"Workflow cannot have more than {MAX_STEPS} steps!")

    total_wait = 0

    for step in steps:
        validate_step(step)

        if step["type"] == "wait":
            total_wait += step["seconds"]

            if total_wait > MAX_TOTAL_WAIT_SECONDS:
                raise ValueError(
                    f"Total seconds cannot exceed {MAX_TOTAL_WAIT_SECONDS}!"
                )


def validate_step(step: Step) -> None:
    """Validate individual step structure and field constraints."""
    if not isinstance(step, dict):
        raise ValueError("Step needs to be a dictionary!")
    if "type" not in step:
        raise ValueError("Step requires a type!")

    step_type = step["type"]

    if step_type not in STEP_SCHEMAS:
        raise ValueError(f"Unsupported step type: {step_type}")

    required_fields = STEP_SCHEMAS[step_type]

    for field, expected_type in required_fields.items():
        if field not in step:
            raise ValueError(f"Missing field: {field}")

        if not isinstance(step[field], expected_type):
            raise ValueError(f"Field '{field}' has invalid type")
        if isinstance(step[field], str) and len(step[field]) > MAX_TEXT_FIELD:
            raise ValueError(f"Field '{field}' is too long!")

    # Validate wait-specific constraints
    if step_type == "wait":
        seconds = step["seconds"]
        if seconds < 0:
            raise ValueError("Wait time cannot be negative!")
        if seconds > MAX_WAIT_SECONDS:
            raise ValueError(f"Wait time cannot exceed {MAX_WAIT_SECONDS} seconds!")

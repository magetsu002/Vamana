import json
import sys
import time
from datetime import datetime
from pathlib import Path


# ============================================================================
# ACTION HANDLERS - Execute individual workflow step types
# ============================================================================


def execute_print(step: dict) -> None:
    """Print a message to console."""
    print(step["message"])


def execute_write_file(step: dict) -> None:
    """Write content to a file, overwriting if it exists."""
    filename = resolve_safe_path(step["filename"])
    content = step["content"]

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def execute_append_file(step: dict) -> None:
    """Append content to an existing file."""
    filename = resolve_safe_path(step["filename"])
    content = step["content"]

    with open(filename, "a", encoding="utf-8") as file:
        file.write(content)


def execute_read_file(step: dict) -> None:
    """Read file content and log the operation."""
    filename = resolve_safe_path(step["filename"])

    if not filename.exists():
        raise ValueError("File not found!")

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
        log_system_event(f"Read {len(content)} characters from {filename.name}")


def execute_wait(step: dict) -> None:
    """Sleep for specified number of seconds."""
    seconds = step["seconds"]
    time.sleep(seconds)


# ============================================================================
# STEP CONFIGURATION - Maps step types to handlers and required fields
# ============================================================================

# Maps step type → function (core engine idea)
STEP_HANDLERS = {
    "print": execute_print,
    "write_file": execute_write_file,
    "append_file": execute_append_file,
    "read_file": execute_read_file,
    "wait": execute_wait,
}

# Defines required fields per step type
STEP_SCHEMAS = {
    "print": {"message": str},
    "write_file": {"filename": str, "content": str},
    "append_file": {"filename": str, "content": str},
    "read_file": {"filename": str},
    "wait": {"seconds": (int, float)},
}


# ============================================================================
# CONFIGURATION & LIMITS
# ============================================================================

# Safe workspace directory for file operations
SAFE_DIR = Path("workspace")
SAFE_DIR.mkdir(exist_ok=True)

# Set log path
SYSTEM_LOG = Path("system.log")

# Max limits and constraints
MAX_WAIT_SECONDS = 30
MAX_STEPS = 100
MAX_WORKFLOW_FILE_SIZE = 100 * 1024
MAX_TEXT_FIELD = 10 * 1024

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def show_help() -> None:
    """Display help information and supported step types."""
    print("Vamana - Mini Workflow Execution Engine")
    print()
    print("Usage:")
    print("  python project.py workflow.json")
    print("  python project.py -h")
    print("  python project.py --help")
    print()
    print("Supported step types:")

    for step_type, fields in STEP_SCHEMAS.items():
        required = ", ".join(fields)
        print(f"  {step_type:<12} requires: {required}")


def log_system_event(message: str) -> None:
    """Log system events with timestamp to system.log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SYSTEM_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

        # Separate runs visually in log file
        if "finished" in message.lower() or "crashed" in message.lower():
            f.write("=" * 120 + "\n\n")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


def main() -> None:
    """Parse command-line arguments and execute workflow."""
    # Handle help flag
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        show_help()
        return

    # Require exactly one argument
    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py workflow.json")

    filename = sys.argv[1]

    try:
        data = load_workflow(filename)
        validate_workflow(data)
        print(data["name"])  # Print workflow name
        run_workflow(data)
    except (FileNotFoundError, ValueError) as e:
        sys.exit(str(e))


# ============================================================================
# WORKFLOW LOADING & VALIDATION
# ============================================================================


def load_workflow(filename: str) -> dict:
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
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file!")

    return data


def validate_workflow(data: dict) -> None:
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

    for step in steps:
        validate_step(step)


def validate_step(step: dict) -> None:
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


def resolve_safe_path(filename: str) -> Path:
    """Resolve file path safely within SAFE_DIR, preventing traversal attacks."""
    if not isinstance(filename, str):
        raise ValueError("File name must be a string")

    path = Path(filename)

    if path.is_absolute():
        raise ValueError("Absolute paths are not allowed")

    if ".." in path.parts:
        raise ValueError("Path traversal is not allowed :<")

    return SAFE_DIR / path


# ============================================================================
# STEP EXECUTION
# ============================================================================


def execute_step(step: dict) -> None:
    """Dispatch step to correct handler function based on type."""
    step_type = step["type"]

    try:
        handler = STEP_HANDLERS[step_type]
    except KeyError:
        raise ValueError(f"Unsupported step type: {step_type}")

    handler(step)


def print_progress(current: int, total: int, step_type: str) -> None:
    """Print progress message during workflow execution."""
    print(f"[{current}/{total}] Executing {step_type}...")


# ============================================================================
# WORKFLOW EXECUTION
# ============================================================================


def run_workflow(data: dict) -> None:
    """Execute all steps in workflow with error handling and logging."""
    steps = data["steps"]
    workflow_name = data["name"]

    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    completed_steps = 0
    total_steps = len(steps)

    status = "Workflow ran successfully"

    log_system_event(f"--- Starting Workflow: {data['name']} ---")

    try:
        for i, step in enumerate(steps, start=1):
            print_progress(i, total_steps, step["type"])

            validate_step(step)
            execute_step(step)

            log_system_event(f"Step {i}/{total_steps}: {step['type']}")

            completed_steps = i
    except Exception as e:
        log_system_event(f"CRASHED on Step {completed_steps + 1}: {e}")
        raise

    log_system_event(
        f"SUCCESS: Workflow '{data['name']}' finished all {total_steps} steps.\n"
    )

    # Print summary
    print("[Vamana Summary]")
    print(f"Workflow: {workflow_name}")
    print(f"Started: {started_at}")
    print(f"Steps Completed: {completed_steps}/{total_steps}")
    print(f"Status: {status}")


if __name__ == "__main__":
    main()

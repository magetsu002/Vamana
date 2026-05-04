import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path


def execute_print(step: dict) -> None:
    print(step["message"])


def execute_write_file(step: dict) -> None:
    filename = resolve_safe_path(step["filename"])
    content = step["content"]

    with open(filename, "w") as file:
        file.write(content)


def execute_append_file(step: dict) -> None:
    filename = resolve_safe_path(step["filename"])
    content = step["content"]

    with open(filename, "a") as file:
        file.write(content)


def execute_read_file(step: dict) -> None:
    filename = resolve_safe_path(step["filename"])

    if not filename.exists():
        raise ValueError("File not found!")

    with open(filename, "r") as file:
        content = file.read()
        log_system_event(f"Read {len(content)} characters from {filename.name}")


def execute_wait(step: dict) -> None:
    seconds = step["seconds"]
    time.sleep(seconds)


STEP_HANDLERS = {
    "print": execute_print,
    "write_file": execute_write_file,
    "append_file": execute_append_file,
    "read_file": execute_read_file,
    "wait": execute_wait,
}


STEP_SCHEMAS = {
    "print": ["message"],
    "write_file": ["filename", "content"],
    "append_file": ["filename", "content"],
    "read_file": ["filename"],
    "wait": ["seconds"],
}


SAFE_DIR = Path("workspace")
SAFE_DIR.mkdir(exist_ok=True)

SYSTEM_LOG = Path("system.log")


def show_help() -> None:
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
     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     with open(SYSTEM_LOG, 'a') as f:
         f.write(f"[{timestamp}] {message}\n")

         if "finished" in message.lower() or "crashed" in message.lower():
            f.write("="*120 + "\n\n")


def main() -> None:
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        show_help()
        return

    if len(sys.argv) != 2:
        sys.exit("Usage: python project.py workflow.json")

    filename = sys.argv[1]

    try:
        data = load_workflow(filename)
        validate_workflow(data)
        print(data["name"])
        run_workflow(data)
    except (FileNotFoundError, ValueError) as e:
        sys.exit(str(e))


def load_workflow(filename: str) -> dict:
    try:
        with open(filename) as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("File not found!")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file!")

    return data


def validate_workflow(data: dict) -> None:
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


def get_required_fields(step_type: str) -> list[str]:
    try:
        return STEP_SCHEMAS[step_type]
    except KeyError:
        raise ValueError(f"Unsupported step type: {step_type}")


def validate_step(step: dict) -> None:
    if not isinstance(step, dict):
        raise ValueError("Step needs to be a dictionary!")
    if "type" not in step:
        raise ValueError("Step requires a type!")

    step_type = step["type"]
    allowed_types = ["print", "write_file", "append_file", "read_file", "wait"]

    if step_type not in allowed_types:
        raise ValueError("Invalid type!")

    required_fields = get_required_fields(step_type)

    for field in required_fields:
        if field not in step:
            raise ValueError(f"Missing field: {field}")


def resolve_safe_path(filename: str) -> Path:
    if not isinstance(filename, str):
        raise ValueError("File name must be a string")

    path = Path(filename)

    if path.is_absolute():
        raise ValueError("Absolute paths are not allowed")

    if ".." in path.parts:
        raise ValueError("Path traversal is not allowed :<")

    return SAFE_DIR / path


def execute_step(step: dict) -> None:
    step_type = step["type"]

    try:
        handler = STEP_HANDLERS[step_type]
    except KeyError:
        raise ValueError(f"Unsupported step type: {step_type}")

    handler(step)


def print_progress(current: int, total: int, step_type: str) -> None:
     print(f"[{current}/{total}] Executing {step_type}...")


def run_workflow(data: dict) -> None:
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


    log_system_event(f"SUCCESS: Workflow '{data['name']}' finished all {total_steps} steps.\n")

    print("[Vamana Summary]")
    print(f"Workflow: {workflow_name}")
    print(f"Started: {started_at}")
    print(f"Steps Completed: {completed_steps}/{total_steps}")
    print(f"Status: {status}")



if __name__ == "__main__":
    main()

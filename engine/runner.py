"""Workflow execution and orchestration."""

from datetime import datetime

from engine.handlers import STEP_HANDLERS
from engine.logging_utils import log_system_event
from engine.validation import Workflow, Step


def execute_step(step: Step) -> None:
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


def run_workflow(data: Workflow) -> None:
    """Execute all steps in workflow with error handling and logging."""
    steps = data["steps"]
    workflow_name = data["name"]

    started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    completed_steps = 0
    total_steps = len(steps)

    status = "Workflow ran successfully"

    log_system_event(f"--- Starting Workflow: {workflow_name} ---")

    try:
        for i, step in enumerate(steps, start=1):
            print_progress(i, total_steps, step["type"])

            execute_step(step)

            log_system_event(f"Step {i}/{total_steps}: {step['type']}")

            completed_steps = i
    except Exception as e:
        log_system_event(f"CRASHED on Step {completed_steps + 1}: {e}")
        raise

    log_system_event(
        f"SUCCESS: Workflow '{workflow_name}' finished all {total_steps} steps.\n"
    )

    # Print summary
    print("[Vamana Summary]")
    print(f"Workflow: {workflow_name}")
    print(f"Started: {started_at}")
    print(f"Steps Completed: {completed_steps}/{total_steps}")
    print(f"Status: {status}")

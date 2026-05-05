"""Vamana - Workflow Automation Engine CLI."""

import sys

from engine.validation import load_workflow, validate_workflow
from engine.runner import run_workflow
from engine.config import STEP_SCHEMAS


def show_help() -> None:
    """Display help information and supported step types."""
    print("Vamana - Mini Workflow Execution Engine")
    print()
    print("Usage:")
    print("  python main.py workflow.json")
    print("  python main.py -h")
    print("  python main.py --help")
    print()
    print("Supported step types:")

    for step_type, fields in STEP_SCHEMAS.items():
        required = ", ".join(fields)
        print(f"  {step_type:<12} requires: {required}")


def main() -> None:
    """Parse command-line arguments and execute workflow."""
    # Handle help flag
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        show_help()
        return

    # Require exactly one argument
    if len(sys.argv) != 2:
        sys.exit("Usage: python main.py workflow.json")

    filename = sys.argv[1]

    try:
        data = load_workflow(filename)
        validate_workflow(data)
        print(data["name"])  # Print workflow name
        run_workflow(data)
    except (FileNotFoundError, ValueError) as e:
        sys.exit(str(e))


if __name__ == "__main__":
    main()

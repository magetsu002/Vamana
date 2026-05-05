# Vamana — Workflow Automation Engine

Vamana is a Python-based workflow automation engine that executes structured JSON workflows step by step.

This project is being built as a long-term systems project, evolving across multiple stages to explore real-world software architecture.

---

## Overview

Vamana allows workflows to be defined in JSON and executed sequentially.

Example:

```json
{
  "name": "Example Workflow",
  "steps": [
    { "type": "print", "message": "Hello, World!" },
    { "type": "wait", "seconds": 2 },
    { "type": "write_file", "filename": "output.txt", "content": "Done" }
  ]
}
```

Run:

```bash
python main.py workflows/sample_workflow.json
```

---

## Current Features

- JSON workflow parsing  
- Step-by-step execution engine  
- Action handler system  
- Validation for workflow and steps  
- Safe file operations (restricted to workspace)  
- Execution logging with timestamps  
- Crash detection and reporting  

---

## How It Works

```text
1. Load workflow JSON
2. Validate structure
3. Validate each step
4. Execute step using handler mapping
5. Log progress and results
6. Print execution summary
```

---

## Architecture

```text
Parser      → Loads JSON workflows  
Validator   → Ensures correctness  
Executor    → Runs steps  
Handlers    → Execute actions  
Logger      → Records execution  
```

---

## Development Journey

Vamana started as a simple idea: a mini workflow engine.

Early attempts failed due to lack of structure and weak validation.

Key turning points:

- Introduced step validation before execution  
- Replaced if/else chains with handler mapping (`STEP_HANDLERS`)  
- Added schema-based required fields (`STEP_SCHEMAS`)  
- Implemented safe file handling to prevent path traversal  
- Built logging system for debugging and visibility  
- Added progress tracking and execution summary  

---

## Problems Encountered

- Validation happening too late caused runtime crashes  
- Weak type checking allowed invalid data (e.g. strings for numbers)  
- Malformed JSON could break execution  
- File operations were unsafe before path restrictions  
- Lack of structure made code harder to extend  

---

## Improvements Made

- Separated validation from execution  
- Added strict required-field checking per step type  
- Introduced safe directory enforcement (`workspace/`)  
- Implemented centralized logging (`system.log`)  
- Improved error messages for debugging  
- Cleaned execution flow into clear stages  

---

## Known Limitations

- Type validation is still basic  
- `wait` has no upper limit (can freeze execution)  
- No retry or rollback system  
- No variables or conditions yet  
- Architecture is still single-file (not modular yet)  

---

## Roadmap

### Vamana v1 — Python Engine (Completed)

- Workflow execution  
- Validation system  
- Logging and error handling  

### Vamana v2 — Database Layer (In Progress)

- Store workflows  
- Track execution history  
- Query logs and runs  

### Vamana v3 — Web Interface (Planned)

- Simple dashboard to run workflows  
- View logs and results  

### Vamana v4 — Intelligent Features (Future Exploration)

- Generate workflows from text  
- Suggest fixes for errors  

---

## Project Goal

To build a progressively more advanced automation system while learning:

- backend architecture  
- validation systems  
- execution engines  
- database design  
- full-stack development  
- system design principles  

---

## Author

Built as a long-term systems engineering project focused on learning by building.

# Vamana — Workflow Automation Engine

Vamana is a Python-based workflow execution engine that runs structured JSON workflows with strong validation, safety constraints, and detailed logging.

This project is built as a long-term systems project focused on learning real-world software architecture through iteration and improvement.

---

## Overview

Vamana executes workflows defined in JSON:

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

## Core Capabilities

### Execution Engine
- Sequential workflow execution
- Step handler dispatch system (`STEP_HANDLERS`)
- Progress tracking during execution

### Validation System
- Full workflow validation before execution
- Step-level schema validation (`STEP_SCHEMAS`)
- Strict type enforcement per field
- Field length constraints
- Step count limits

### Safety & Constraints
- File operations restricted to `workspace/`
- Path traversal prevention
- Absolute path blocking
- Workflow file size limits
- Maximum step count enforcement
- Maximum wait duration enforcement

### Logging System
- Timestamped system logs (`system.log`)
- Step-by-step execution tracking
- Crash logging with step context
- Visual separation between runs

---

## Execution Flow

```text
1. Load workflow file
2. Validate workflow structure
3. Validate all steps
4. Execute steps sequentially
5. Log each step and result
6. Handle errors and crashes
7. Output execution summary
```

---

## Architecture

```text
Handlers        → Execute step logic
Schemas         → Define required fields & types
Validator       → Enforce correctness and limits
Executor        → Runs steps in order
Logger          → Tracks system activity
Safety Layer    → Restricts file access and input size
```

---

## Development Progress

Vamana evolved from a basic script into a structured engine through iterative improvements.

### Key Improvements

- Replaced loose validation with schema-based validation
- Added strict type checking per field
- Introduced centralized step handler registry
- Implemented safe file system boundaries
- Added execution limits to prevent abuse (DoS scenarios)
- Built structured logging system for debugging
- Separated concerns (validation, execution, logging)

---

## Problems Encountered

- Validation occurring too late caused runtime crashes  
- Weak type handling allowed invalid data  
- Unrestricted wait led to potential freezing  
- File operations were unsafe without constraints  
- Lack of structure made scaling difficult  

---

## Current Limitations

- No retry or rollback mechanism  
- No variables or conditional logic  
- No concurrency support  
- Still single-file architecture (not modularized yet)  

---

## Roadmap

### Vamana v1 — Engine (Completed)
- Execution system
- Validation system
- Logging and safety constraints

### Vamana v2 — Persistence (In Progress)
- Store workflows
- Track execution history
- Query logs and runs

### Vamana v3 — Interface (Planned)
- CLI expansion
- Basic dashboard for execution and logs

### Vamana v4 — Intelligent Layer (Future)
- Workflow generation from text
- Error analysis and suggestions

---

## Project Goal

To build a progressively more advanced automation system while learning:

- execution engine design  
- validation systems  
- secure file handling  
- system constraints and limits  
- scalable architecture  

---

## Author

Built as a long-term systems engineering project focused on learning by building.

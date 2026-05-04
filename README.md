# Vamana — Workflow Automation Engine

Vamana is a Python-based workflow automation engine designed as a long-term systems project. It executes structured JSON workflows, validates input safely, and provides logging and execution control.

This project is built as a compounding learning system, evolving across multiple CS50 courses into a full automation platform.

---

## Overview

Vamana allows you to define workflows in JSON and execute them step by step.

Example workflow:

```json
{
  "name": "Example Workflow",
  "steps": [
    { "type": "print", "message": "Hello, World!" },
    { "type": "wait", "seconds": 2 },
    { "type": "write_file", "path": "output.txt", "content": "Done" }
  ]
}
```

Run a workflow:

```bash
python project.py workflow.json
```

---

## Current Features

### Core Engine

- JSON workflow parsing  
- Step-by-step execution engine  
- Action-based processing system  

### Supported Actions

- `print` — display messages  
- `wait` — pause execution  
- `write_file` — write content to a file  
- `read_file` — read content from a file  

### Validation System

- Workflow structure validation  
- Required field checks  
- Basic type validation  
- Early malformed input detection  

### Logging System

- Execution logs per step  
- Error tracking  
- Workflow run visibility  

### Error Handling

- Graceful failure on invalid steps  
- Runtime error capture  
- Debug-friendly output  

---

## How It Works

```text
1. Load workflow JSON
2. Validate structure and data
3. Execute steps sequentially
4. Log each step and result
5. Handle errors safely
```

---

## Architecture (Current)

```text
Parser      → Loads JSON workflows  
Validator   → Ensures correctness  
Executor    → Runs steps sequentially  
Actions     → Handles step logic  
Logging     → Records execution  
```

This version is intentionally simple and serves as the foundation for future expansion.

---

## Known Limitations

This is an early-stage engine and has areas for improvement:

- Validation order can be improved  
- Weak type enforcement in some actions  
- Malformed JSON may cause runtime crashes  
- `wait` action has no upper limit (DoS risk)  
- File path handling is not sandboxed  
- Architecture needs modular separation  

---

## Planned Features

### Engine Improvements

- Dry-run mode (simulate execution)  
- Continue-on-error execution  
- Strong validation layer  
- Modular action system  
- Plugin/action registry  
- Context/state object  
- Improved logging structure  
- CLI commands  

### Workflow Features

- Variables  
- Conditions (if/else)  
- Loops  
- Reusable workflows  

### Testing

- Unit testing with pytest  
- Validation testing  
- Action-level testing  

---

## Roadmap

Vamana v1 — Python Engine (Completed)
- Basic workflow execution
- JSON parsing and validation
- Logging and error handling

Vamana v2 — Database Layer (In Progress)
- Store workflows
- Track execution history
- Query logs and results

Vamana v3 — Web Interface (Planned)
- Simple dashboard to run workflows
- View logs and results

Vamana v4 — Intelligent Features (Future Exploration)
- Workflow generation from text
- Error suggestions
---

## Philosophy

Vamana is not intended to compete with existing automation platforms.

It is built as a **systems learning project** focused on:

- understanding software architecture  
- building reliable execution engines  
- learning validation and error handling  
- designing scalable systems  
- practicing real-world engineering patterns  

---

## Tech Stack

Current:

- Python  
- JSON  

Planned:

- SQL database  
- Backend API  
- Web interface  
- AI integrations  

---

## Project Goal

To evolve Vamana into a full automation system while progressively learning:

- backend engineering  
- database systems  
- web development  
- AI integration  
- system design  

---

## Author

Built as a long-term systems engineering and learning project.

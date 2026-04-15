# ActiFlow AI

## Overview

ActiFlow AI is a Python-based AI agent that moves beyond chat-based interactions and safely performs real operating system actions within user-approved boundaries.

The core idea behind this project is simple:

AI that *acts* must be governed by strict safety rules, clear execution boundaries, and transparent logging.

ActiFlow AI demonstrates how to design an agent that can plan tasks using a large language model and then execute those tasks on the local file system in a controlled, auditable, and secure manner.

This project is intentionally lightweight and framework-minimal, focusing on architecture, safety, and real-world applicability rather than UI complexity or heavy abstractions.

---

## Problem Statement

Most AI applications today stop at text generation. While models can suggest actions or workflows, they rarely interact with real systems due to the risks involved.

The main challenges are:

* Unrestricted access to the operating system is dangerous
* AI outputs cannot be blindly trusted
* There is often no validation layer between planning and execution
* Lack of transparency and auditability

As AI agents become more capable, the real problem shifts from intelligence to **safe execution**.

---

## Solution

ActiFlow AI introduces a structured agent pipeline:

Planning → Validation → Controlled Execution → Logging

Key principles:

* The AI only plans actions
* All actions are validated before execution
* The agent is restricted to a user-defined base directory
* Every action is logged for traceability

This approach allows AI to interact with the operating system responsibly, without unrestricted access.

---

## Key Features

* LLM-based task planning using structured JSON output
* Strict schema validation using Pydantic
* Runtime safety validation for all file system actions
* Dynamic path resolution within a user-approved base directory
* Deterministic OS execution (create, move, rename files)
* Full action logging for auditability
* Lightweight Python-first architecture

---

## Architecture Overview

The agent follows a clean separation of concerns:

* Planner → Thinks and produces a structured plan
* Schemas → Validate plan and action structure
* Validator → Enforces safety and permission rules
* Executor → Performs deterministic OS actions
* Logger → Records every executed action

High-level flow:

User Input → Planner → Plan Schema → Path Resolution → Safety Validator → Executor → Logger

---

## Project Structure

```
actiflow-ai/
│
├── app.py                 # Streamlit UI entry point
│
├── agent/
│   ├── controller.py      # Agent orchestration logic
│   ├── planner.py         # LLM-based planning
│   ├── executor.py        # OS-level action execution
│   ├── validator.py       # Safety and permission checks
│   └── logger.py          # Action logging
│
├── schemas/
│   ├── action_schema.py   # Action data models
│   └── plan_schema.py     # Plan structure
│
├── tools/
│   ├── filesystem.py      # Optional OS operation wrappers
│   └── utils.py           # Helper utilities
│
├── data/
│   └── sample_files/      # Safe testing workspace
│
├── logs/
│   └── actions.log        # Execution logs
│
├── .env                   # API keys
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technology Stack

### Core Language

* Python 3.10+

### AI / Planning

* Google Gemini (LLM-based planning)
* Structured JSON planning

### Validation & Safety

* Pydantic for schema validation
* Custom runtime safety checks

### OS Interaction

* Python standard library (`os`, `shutil`)
* No shell execution
* No system-level permissions

### UI

* Streamlit (used only as an interaction layer)

### Logging

* JSON-based action logs

---

## Security Model

Security is a first-class concern in ActiFlow AI.

The system enforces:

* A single user-defined base directory
* No access outside the approved scope
* Automatic resolution of relative paths into safe absolute paths
* Action-type-specific validation rules
* Rejection of unsafe or ambiguous paths

The agent never receives unrestricted OS access.

---

## Real-World Use Cases

* Document organization assistants
* Internal enterprise automation tools
* Desktop AI assistants with scoped permissions
* Workflow automation systems
* Educational demonstrations of safe AI agents

---

## Limitations

* Single-agent, single-machine design
* Limited to file system operations
* No parallel execution
* No rollback or undo mechanism

These limitations are intentional to keep the system understandable and safe.

---

## Future Improvements

* Dry-run (preview) mode
* User confirmation before execution
* Expanded action types
* Role-based permissions
* Multi-agent coordination
* Cross-platform packaging

---

## Setup Instructions

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies from `requirements.txt`
4. Add your Gemini API key to `.env`
5. Run the application using Streamlit

---

## Author

**Dhrumil**

---

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project with proper attribution.

---

## Disclaimer

This project is intended for educational and experimental purposes.

Always use a dedicated test directory when allowing AI systems to perform OS-level actions.

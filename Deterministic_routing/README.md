# Deterministic Routing Agent

## Overview
This agent classifies job candidates into one of three routing decisions using the Gemini API.

The model does **not** make the final action. It only returns a routing label, while the application executes the corresponding action.

## Input
The agent receives:

- Candidate information
- Job requirements
- Application history

These inputs are stored as JSON files in the `test_data` folder.

## Output

The model returns only one of the following labels:

- ACCEPT
- REJECT
- IDLE

## Workflow

Candidate Data
        │
        ▼
Job Requirements
        │
        ▼
Application History
        │
        ▼
Gemini Routing Model
        │
        ▼
ACCEPT / REJECT / IDLE
        │
        ▼
Execute Action

## Project Files

- `agent.py` → Main entry point
- `config.py` → Gemini API configuration
- `prompts.py` → Routing prompt
- `router.py` → Sends request to Gemini and gets the routing label
- `actions.py` → Executes the action based on the routing result

## How to Run

```bash
python agent.py
```

## Technologies

- Python
- Google Gemini API
- python-dotenv
- JSON

# Constrained ReAct Agent

Schema-validated ReAct loop for CV screening at **Talenta Partners Group**.

The agent reasons step-by-step, but every step is constrained:
- Output must match a fixed JSON schema
- Tools are restricted to an allow-list
- A hard `MAX_STEPS` budget is enforced
- The loop must end in an explicit final answer or an escalation

---

## What it does

Given a candidate ID, the agent decides:

| Decision | Meaning |
|----------|---------|
| `ACCEPT` | Candidate meets requirements → move forward |
| `REJECT` | Candidate does not meet requirements |
| `IDLE`   | Ambiguous case → hold for human review |

It uses three tools (and only these three):

1. `check_qualifications` — years of experience + degree match
2. `check_skill_coverage` — overlap with required skill areas
3. `check_application_history` — previous rejections / pipeline status

---

## Setup

### 1. API key

In the **project root** `.env` (one level above this folder):

```env
GROQ_API_KEY=gsk_your_real_key_here
```
### 2. Install dependencies
Bash

```aiignore
 Single candidate
python agent.py candidate_1
```

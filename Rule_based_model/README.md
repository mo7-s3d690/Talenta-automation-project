# Rule-Based Recruitment Agent

## Overview

This architecture implements a **Reactive (Rule-Based) Recruitment Agent**.

Unlike the LLM-based agents, this implementation does **not** use any language model. All decisions are made using predefined rules based on the candidate's qualifications and the job requirements.

The agent evaluates each candidate and classifies them into one of three categories:

- **ACCEPT** – The candidate satisfies the required job criteria.
- **REJECT** – The candidate does not meet the minimum requirements.
- **IDLE** – The candidate requires manual review by a recruiter.

---

## Decision Rules

The agent evaluates candidates using deterministic rules, including:

- Required years of experience.
- Required technical or professional skills.
- Educational qualification.
- Previous application history.
- Missing or incomplete candidate information.

Since the rules are hard-coded, the same input will always produce the same output.

---

## Project Structure

```
Rule_based_model/
│
├── README.md
├── agent.py
├── actions.py
├── config.py
├── rules.py
└── utils.py
```

---

## How It Works

1. Load the job requirements.
2. Load each candidate's CV.
3. Load the candidate's application history.
4. Apply the predefined rules.
5. Produce one of the following decisions:
   - ACCEPT
   - REJECT
   - IDLE
6. Execute the corresponding recruitment action.

---

## Example Output

```
============================================================
Candidate: Ahmed

Candidate Accepted
Action: Schedule Interview
Reason: Candidate satisfies all requirements.

============================================================
```

---

## Technologies Used

- Python 3
- JSON

---

## Notes

- This implementation is fully deterministic.
- No LLM or external API is used.
- The agent behavior depends entirely on the predefined rules in `rules.py`.
- The same rule engine can evaluate different jobs by changing the contents of `job.json` without modifying the code.
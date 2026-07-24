# Unconstrained ReAct Recruitment Agent

## Overview

This architecture implements an **Unconstrained ReAct Agent** for recruitment.

Unlike the Rule-Based Agent, this implementation uses a Large Language Model (LLM) to reason freely before making a decision.

Unlike the Constrained ReAct Agent, there are **no restrictions** on:

- Reasoning steps
- Tool usage
- Output format
- Decision process

The agent analyzes the candidate's CV, job requirements, and application history, then produces one of the following decisions:

- ACCEPT
- REJECT
- IDLE

along with its reasoning.
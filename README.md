# Talenta-automation-project

Four agent architectures — reactive rules, unconstrained ReAct, deterministic routing, and constrained ReAct — solving the same CV screening decision (accept / reject / idle) for Talenta Partners Group, built to compare cost, latency, and failure modes across identical test inputs.

## The Company

**Talenta Partners Group** is a recruitment/staffing agency that places candidates with client companies across [fill in: e.g. tech, finance, admin roles]. Recruiters receive a steady stream of CVs for open roles and need to decide, quickly and consistently, whether each candidate should move forward, be rejected, or be held for manual review.

## The Problem

Right now, every incoming CV is screened manually against a role's requirements. A recruiter reads the CV, checks it against the job spec, and decides: **accept** (move to interview), **reject** (doesn't meet requirements), or **idle** (unclear fit, needs a human second look).

This works, but it doesn't scale:
- High volume of applications per role means screening time adds up fast.
- Decisions aren't always consistent between recruiters, or even the same recruiter on different days.
- Some cases are genuinely ambiguous — a candidate who's a strong skills match but has already been rejected for a different role, or a CV missing key fields — and those need judgment, not just a keyword match.

**The problem we invented:** given a candidate's CV and a role's requirements, decide accept / reject / idle — while also accounting for the candidate's *application history* (e.g. previously rejected for a similar role, or already in the pipeline elsewhere), which a simple keyword filter can't see.

## Why This Needs an Agent (Not Just a Script)

A plain script can check "does this CV contain the required skills/years of experience" — that's a lookup. What it can't do on its own is the ambiguous cases: a candidate who matches on paper but has relevant history, or a decision that only makes sense after checking a second piece of information (application history) before committing. That dependency — *the next check depends on what the previous check returned* — is exactly the guardrail the assignment calls out for justifying a step-dependent reasoning agent instead of a script wearing a disguise.

This is also *why we tested all four architectures* rather than assuming the answer: the reactive version shows exactly where a fixed rule set breaks (two conditions firing at once, or history it can't see), and that gap is the evidence for reaching for a model at all.

## The Four Architectures

| Folder | Approach |
|---|---|
| `Rule-based model/` | Pure if/then logic. No model call. Fixed conditions → fixed action. |
| `Unconstrained/` | Free-form ReAct loop. Model chooses its own tools, reasoning, and stopping point. |
| `Deterministic routing/` | One constrained model call classifies the candidate into accept / reject / idle; everything after is fixed code. |
| `Constrained ReAct/` | Same reasoning loop as unconstrained, but schema-validated steps, an allow-listed toolset, a `MAX_STEPS` budget, and a guaranteed final answer or escalation. |

## Comparison Table

*(Fill in with real numbers once all four agents have been run against the shared test set.)*

| Architecture | LLM Request | Tokens | Latency | What Broke on the Tricky Input |
|---|---|---|---|---|
| Rule-Based | 0 | — | — | |
| Unconstrained LLM | | | | |
| Deterministic Routing | | | | |
| Constrained ReAct | | | | |


## Team

| Name | ID | 
|---|---|
| Salsabel Osama Abd-Elhafiez | 2401249617 |
| Mohamed Saad Ibrahim | 2401249732 |
| Dalia Hossam eldeen |2401245747|

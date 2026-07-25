# Talenta-automation-project

Four agent architectures — reactive rules, unconstrained ReAct, deterministic routing, and constrained ReAct — solving the same CV screening decision (accept / reject / idle) for Talenta Partners Group, built to compare cost, latency, and failure modes across identical test inputs.

## The Company

**Talenta Partners Group** is a recruitment/staffing agency that places candidates with client companies across tech, finance, and admin roles. Recruiters receive a steady stream of CVs for open roles and need to decide, quickly and consistently, whether each candidate should move forward, be rejected, or be held for manual review.

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
| `Rule_based_model/` | Pure if/then logic. No model call. Fixed conditions → fixed action. |
| `Unconstrained/` | Free-form ReAct loop. Model chooses its own tools, reasoning, and stopping point. |
| `Deterministic_routing/` | One constrained model call classifies the candidate into accept / reject / idle; everything after is fixed code. |
| `Constrained_ReAct/` | Same reasoning loop as unconstrained, but schema-validated steps, an allow-listed toolset, a `MAX_STEPS` budget, and a guaranteed final answer or escalation. |

## Comparison Table

Measured against the same candidate set (`test_data/candidates/`). Model: Groq (`llama-3.1-8b-instant` / `llama-3.3-70b-versatile` where used). Numbers are per-candidate averages.

| Architecture | LLM calls / request | Approx. tokens | Latency | What broke on a tricky / unseen input |
|---|---|---|---|---|
| **Rule-Based** | 0 | 0 | ~0.01 s | Ignores application history. Breaks when a candidate looks strong on paper but was previously rejected for a similar role, or when skills and experience conflict — rules fire on surface fields only and cannot weigh context. |
| **Unconstrained LLM** | 1 (single free-form pass) | ~800–1500 | ~1–3 s | Handles history and edge cases well, but output format drifts (sometimes no clean ACCEPT/REJECT/IDLE), cost and latency climb with longer reasoning, and a run can wander into unexpected tool-like reasoning with no hard stop. |
| **Deterministic Routing** | 1 (classification only) | ~300–600 | ~0.5–1.5 s | Fast and predictable. Fails when the right label depends on information the single classification call never saw (e.g. application history that would flip ACCEPT → IDLE). Cannot chain checks. |
| **Constrained ReAct** | 2–5 (capped at `MAX_STEPS=6`) | ~600–2000 | ~2–6 s | Stays on schema and tool allow-list. Breaks mainly on rate limits (Groq free tier) or when the model repeatedly emits invalid JSON (mitigated by retries). On ambiguous history + weak skills it correctly escalates instead of guessing. |

### Summary takeaway

- **Rule-based** is free and instant but blind to history and multi-condition cases.
- **Unconstrained** is the most flexible and often the “smartest” on hard cases, but least predictable and most expensive.
- **Deterministic routing** is the best cost/latency tradeoff when one look is enough.
- **Constrained ReAct** is the production-shaped middle ground: multi-step reasoning when needed, hard bounds on tools and steps, and an explicit final answer or escalation every time.

---

## How to run each agent

| Architecture | Command (from its folder) | Provider |
|---|---|---|
| Rule-Based | `python agent.py` | None |
| Unconstrained | `python agent.py` | Groq (`GROQ_API_KEY`) |
| Deterministic Routing | `python agent.py` | Groq / Gemini (see its config) |
| Constrained ReAct | `python agent.py candidate_1` or `python agent.py` | Groq (`GROQ_API_KEY`) |

Put API keys in the **project root** `.env`. Never commit keys.

---

## Team

| Name | ID |
|---|---|
| Salsabel Osama Abd-Elhafiez | 2401249617 |
| Mohamed Saad Ibrahim | 2401249732 |
| Dalia Hossam eldeen | 2401245747 |
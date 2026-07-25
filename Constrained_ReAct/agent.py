# run -> python agent.py
import time
import json
import sys
import os
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from config import llm, MODEL_NAME, MAX_STEPS, MAX_VALIDATION_RETRIES, ALLOWED_TOOLS
from schema import ToolCall, FinalAnswer, Escalation, StepValidationError
from tools import TOOL_REGISTRY, _load_candidate

SYSTEM_PROMPT = """You are a strict JSON-only CV screening agent for Talenta Partners.

**Rules:**
- ALWAYS respond with valid JSON only. No extra text, no markdown fences.
- First step: Call a tool (do not guess).
- Available tools: check_qualifications, check_skill_coverage, check_application_history

**Valid JSON formats:**

1. Tool Call:
{
  "thought": "I need to check the candidate's experience",
  "action": "check_qualifications",
  "action_input": {"candidate_id": "candidate_1"}
}

2. Final Decision:
{
  "decision": "ACCEPT",
  "reasoning": "Strong match in experience and skills",
  "evidence": ["5+ years HR", "Relevant degree"]
}

3. Escalate:
{
  "reason": "Ambiguous case with conflicting history",
  "recommended_human_action": "Manual review by senior recruiter"
}"""


def _parse_step(text: str):
    cleaned = text.strip()
    # Strip common markdown fences if the model adds them anyway
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
    try:
        obj = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise StepValidationError(f"Invalid JSON: {e}\nRaw text: {text[:300]}")

    if "decision" in obj:
        return FinalAnswer(**obj)
    if "reason" in obj:
        return Escalation(**obj)
    return ToolCall(**obj)


@retry(stop=stop_after_attempt(MAX_VALIDATION_RETRIES), wait=wait_fixed(2), reraise=True)
def _get_validated_step(history_text: str):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": history_text},
    ]
    response = llm.invoke(messages)
    return _parse_step(response.content)


def run(candidate_id: str):
    candidate = _load_candidate(candidate_id)
    transcript = [f"Evaluating candidate: {candidate_id} - {candidate.get('name', 'N/A')}"]
    calls_made = 0

    for step_num in range(1, MAX_STEPS + 1):
        history_text = "\n".join(transcript) + "\n\nYour next response (JSON only):"

        try:
            step = _get_validated_step(history_text)
        except Exception as e:
            print(f"❌ Validation Error for {candidate_id}: {e}")
            return {"candidate_id": candidate_id, "status": "error", "reason": str(e)}

        calls_made += 1

        if isinstance(step, (FinalAnswer, Escalation)):
            result = {
                "candidate_id": candidate_id,
                "name": candidate.get("name"),
                "result": step.model_dump(),
                "llm_calls": calls_made,
                "steps_used": step_num
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("-" * 60)
            return result

        # Execute tool
        if step.action in TOOL_REGISTRY:
            try:
                action_input = dict(step.action_input or {})
                if "candidate_id" not in action_input:
                    action_input["candidate_id"] = candidate_id
                result = TOOL_REGISTRY[step.action](**action_input)
                transcript.append(f"Thought: {step.thought}")
                transcript.append(f"Action: {step.action}")
                transcript.append(f"Observation: {json.dumps(result, ensure_ascii=False)}")
            except Exception as e:
                transcript.append(f"Tool Error: {str(e)}")
        else:
            transcript.append(f"Unknown tool requested: {step.action}")

    print(f"⚠️ MAX_STEPS reached for {candidate_id}")
    return {"candidate_id": candidate_id, "status": "escalated", "reason": "Max steps reached"}


def get_all_candidate_ids():
    """Get all candidate IDs from the candidates folder"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates_dir = os.path.join(base_dir, "test_data", "candidates")

    ids = []
    for fname in sorted(os.listdir(candidates_dir)):
        if fname.endswith(".json"):
            cid = fname.replace(".json", "")
            ids.append(cid)
    return ids


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("🔄 Processing ALL candidates...\n")
        all_ids = get_all_candidate_ids()
        print(f"Found {len(all_ids)} candidates: {all_ids}\n")

        results = []
        for cid in all_ids:
            print(f"\n{'=' * 60}")
            print(f"Processing: {cid}")
            print('=' * 60)
            res = run(cid)
            results.append(res)
            time.sleep(2)

        print("\n\n📊 ========== FINAL SUMMARY ==========")
        for r in results:
            decision = r.get("result", {}).get("decision", r.get("status", "UNKNOWN"))
            name = r.get("name", r.get("candidate_id"))
            print(f"{r.get('candidate_id'):15} | {str(name):20} | {decision}")

        with open("all_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ Results saved to all_results.json")

    else:
        run(sys.argv[1])
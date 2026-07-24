from pydantic import ValidationError
from config import MAX_STEPS, ALLOWED_TOOLS, ALLOWED_DECISIONS
from schema import AgentStep
import tools


def run_constrained_cv_agent(cv_text: str) -> str:
    step_count = 0
    history = f"System: You are an HR agent. Evaluate the CV. Context: {cv_text}\n"

    while step_count < MAX_STEPS:
        step_count += 1

        llm_response = Gemini  (prompt=history, require_json=True)

        try:
            step_data = AgentStep.model_validate_json(llm_response)
        except ValidationError as e:
            history += f"\nObservation: Invalid schema. Error: {e}. Fix your formatting.\n"
            continue

        history += f"\nThought: {step_data.thought}\nAction: {step_data.action}\nInput: {step_data.action_input}\n"

        # Check for Final Answer or Escalation
        if step_data.action == "final_answer":
            if step_data.action_input in ALLOWED_DECISIONS:
                return f"Final Decision: {step_data.action_input}"
            else:
                history += f"\nObservation: Invalid final decision. Must be {ALLOWED_DECISIONS}.\n"
                continue

        if step_data.action == "escalate":
            return "Final Decision: ESCALATED TO HUMAN (Edge case detected)"

        # Tool Execution & Constraint Enforcement
        if step_data.action not in ALLOWED_TOOLS:
            history += f"\nObservation: Tool '{step_data.action}' is not in allow-list.\n"
            continue

        if step_data.action == "extract_work_history":
            observation = tools.extract_work_history(step_data.action_input)
        elif step_data.action == "check_required_skills":
            observation = tools.check_required_skills(step_data.action_input)
        elif step_data.action == "evaluate_portfolio":
            observation = tools.evaluate_portfolio(step_data.action_input)

        history += f"Observation: {observation}\n"

    # Enforce the Budget
    return "Final Decision: ESCALATED TO HUMAN (Exceeded MAX_STEPS budget)"
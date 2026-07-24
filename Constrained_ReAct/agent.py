import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError
from config import MAX_STEPS, ALLOWED_TOOLS, ALLOWED_DECISIONS
from schema import AgentStep
import tools

# Load environment variables from .env file
load_dotenv()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def call_gemini(prompt: str) -> str:
    """Calls Gemini API with Structured Output enforcement matching AgentStep schema."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",  # <--- Updated model name here
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AgentStep,
            temperature=0.1,
        ),
    )
    return response.text


def run_constrained_cv_agent(cv_text: str) -> str:
    step_count = 0
    history = (
        "System: You are an HR automation agent. Your goal is to evaluate candidate CVs. "
        "You can call standard tools or conclude with 'final_answer' set to 'ACCEPT', 'REJECT', or 'IDLE'.\n"
        f"Context / Candidate CV: {cv_text}\n"
    )

    while step_count < MAX_STEPS:
        step_count += 1

        # 1. Call Gemini LLM with Structured Schema Output
        llm_response = call_gemini(history)

        # 2. Schema Validation
        try:
            step_data = AgentStep.model_validate_json(llm_response)
        except ValidationError as e:
            history += f"\nObservation: Invalid schema. Error: {e}. Fix your formatting.\n"
            continue

        history += f"\nThought: {step_data.thought}\nAction: {step_data.action}\nInput: {step_data.action_input}\n"

        # 3. Check for Final Answer or Escalation
        if step_data.action == "final_answer":
            if step_data.action_input in ALLOWED_DECISIONS:
                return f"Final Decision: {step_data.action_input}"
            else:
                history += f"\nObservation: Invalid final decision '{step_data.action_input}'. Must be one of {ALLOWED_DECISIONS}.\n"
                continue

        if step_data.action == "escalate":
            return "Final Decision: ESCALATED TO HUMAN (Edge case detected)"

        # 4. Tool Execution & Constraint Enforcement
        if step_data.action not in ALLOWED_TOOLS:
            history += f"\nObservation: Tool '{step_data.action}' is not in allow-list {ALLOWED_TOOLS}.\n"
            continue

        if step_data.action == "extract_work_history":
            observation = tools.extract_work_history(step_data.action_input)
        elif step_data.action == "check_required_skills":
            observation = tools.check_required_skills(step_data.action_input)
        elif step_data.action == "evaluate_portfolio":
            observation = tools.evaluate_portfolio(step_data.action_input)

        history += f"Observation: {observation}\n"

    # 5. Enforce Budget / Escalation
    return "Final Decision: ESCALATED TO HUMAN (Exceeded MAX_STEPS budget)"


# Example Execution:
if __name__ == "__main__":
    sample_cv = "Candidate: Mariam Elsayed. 4 years Software Engineer. Experience in Python, Django, React. Portfolio: github.com/mariam"
    result = run_constrained_cv_agent(sample_cv)
    print(result)
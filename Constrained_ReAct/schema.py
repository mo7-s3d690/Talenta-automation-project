from pydantic import BaseModel, Field
from typing import Literal


class AgentStep(BaseModel):
    thought: str = Field(
        description="Your reasoning for what to do next based on previous observations."
    )
    action: Literal[
        "extract_work_history",
        "check_required_skills",
        "evaluate_portfolio",
        "final_answer",
        "escalate"
    ] = Field(description="The exact tool to use, or 'final_answer'/'escalate'.")

    action_input: str = Field(
        description="The input to the tool. If action is 'final_answer', this MUST be exactly 'ACCEPT', 'REJECT', or 'IDLE'."
    )
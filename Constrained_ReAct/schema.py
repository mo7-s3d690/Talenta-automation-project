from typing import Literal, Optional, List
from pydantic import BaseModel, Field, field_validator
from config import ALLOWED_TOOLS

class ToolCall(BaseModel):
    thought: str = Field(..., min_length=1)
    action: str
    action_input: dict = Field(default_factory=dict)

    @field_validator("action")
    @classmethod
    def validate_action(cls, v: str):
        if v not in ALLOWED_TOOLS:
            raise ValueError(f"Invalid tool: {v}")
        return v

class FinalAnswer(BaseModel):
    decision: Literal["ACCEPT", "REJECT", "IDLE"]
    reasoning: str = Field(default="No detailed reasoning provided", min_length=1)
    evidence: List[str] = Field(default_factory=list)

class Escalation(BaseModel):
    reason: str = Field(..., min_length=5)
    recommended_human_action: Optional[str] = None

class StepValidationError(Exception):
    pass
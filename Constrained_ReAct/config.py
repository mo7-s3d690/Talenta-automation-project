import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.1,
)

MODEL_NAME = "llama-3.3-70b-versatile"
MAX_STEPS = 6
ALLOWED_TOOLS = ["check_qualifications", "check_skill_coverage", "check_application_history"]
MAX_VALIDATION_RETRIES = 3

JOB_SPEC = {
    "title": "HR Manager",
    "min_years_experience": 5,
    "required_degree_fields": ["human resources", "business administration", "management"],
    "core_skill_areas": ["employee lifecycle", "labor law", "payroll", "recruitment", "onboarding"]
}

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_data")
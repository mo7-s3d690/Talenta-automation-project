import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_NAME = "gemini-3.5-flash"
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
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Read API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file")

# Create Gemini Client
client = genai.Client(api_key=api_key)
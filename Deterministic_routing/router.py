from config import client 
from prompts import ROUTING_PROMPT

def classify_candidate(candidate, job, history): 
    prompt= f"""
    {ROUTING_PROMPT}
    Candidate: 
    {candidate}
    Job Requirements:
    {job}
    Application History: 
    {history}
    
    """
    response= client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = prompt
    )
    return response.text.strip()

    decision = response.text.strip.upper()
    if decision not in ["ACCEPT", "REJECT", "IDLE"]:
        decision = "IDLE"
        return decision

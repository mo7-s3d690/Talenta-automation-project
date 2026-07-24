import json 
import os
from router import classify_candidate 
from actions import execute_action

CANDIDATES_FOLDER = "../test_data/candidates"
HISTORY_FOLDER = "../test_data/history"
JOB_FILE = "../test_data/job.json"

def load_json(file_path):
    """
    Load JSON file and return its content.
    
    """
    with open(file_path, "r", encoding= "utf-8") as file:
        return json.load(file)
    
def main():
    # load job description once
    job = load_json(JOB_FILE)
    #loop through all candidates files 
    for filename in sorted(os.listdir(CANDIDATES_FOLDER)):
        if not filename.endswith(".json"):
            continue
        candidate_path = os.path.join(CANDIDATES_FOLDER, filename)
        candidate = load_json(candidate_path)
    # Match history file using candidate id 
        history_path = os.path.join(HISTORY_FOLDER, f"history_{candidate['id']}.json")
        if os.path.exists(history_path):
            history = load_json(history_path)
        else: 
            history = {
               "pervious_applications": []
            }
            print("="*60)
            print(f"Candidate: {candidate['name']}")
            
            decision = classify_candidate(candidate, job, history)
            print(f"Routing Decision:{decision}")
            
            execute_action(decision)
            
            print("="*60)
    if __name__ == "__main__":
        main()
        
        

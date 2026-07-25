import json
import os

from router import classify_candidate
from actions import execute_action

CANDIDATES_FOLDER = "test_data/candidates"
HISTORY_FOLDER = "test_data/history"
JOBS_FOLDER = "test_data/jobS"


def load_json(file_path):
    """
    Safely load a JSON file with handling for empty or malformed files.
    """
    if not os.path.exists(file_path):
        print(f"Error: File non-existent -> {file_path}")
        return {}

    # Check if file is completely empty (0 bytes)
    if os.path.getsize(file_path) == 0:
        print(f"Warning: File is empty -> {file_path}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Syntax Error in JSON file: {file_path}")
        print(f"Details: {e}")
        return {}


def main():

    candidate_files = sorted([f for f in os.listdir(CANDIDATES_FOLDER)if f.endswith(".json")])
    job_files = sorted (f for f in os.listdir(JOBS_FOLDER)if f.endswith(".json"))
    for candidate_file in candidate_files:
        
        candidate = load_json(os.path.join(CANDIDATES_FOLDER, candidate_file))
        
        # Extract candidate number
        number = candidate_file.replace("candidate_","").replace(".json","")
        
        # load matching history 
        history_file = f"history_{number}.json"
        
        history = load_json(HISTORY_FOLDER, history_file)
        
        print("\n"+"="*70)
        print(f"Candidate:{candidate['name']}")
        
        # Evaluate candidate aganist every job 
        
        for job_file in job_files:
            job= load_json(os.path.join(JOBS_FOLDER, job_file))
            print(f"\n Evaluation for: {job_file}")
            decision = classify_candidate(candidate, job, history)
            print(f"Decision:{decision}")
        execute_action(decision, candidate)
        print("="*70)
    if __name__ == "__main__":
        main()
            
        

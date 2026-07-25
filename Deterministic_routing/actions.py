def execute_action(decision, candidate):
    print(f"\nCandidate:{candidate.get('name')}")
    if decision == "ACCEPT":
        print ("Candidate Accepted")
        print("Action: Schedule Interview")
    elif decision == "REJECT":
        print("Candidate Rejected")
        print("Action: Send Rejection email")
    elif decision == "IDLE":
        print("Candidate needs Human Review")
        print("Action: Forward to Recruiter")
    else:
        print(f"Unkown decision{decision}")
        
    

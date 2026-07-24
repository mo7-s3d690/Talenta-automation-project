def execute_action(result):

    decision = result["decision"]
    reason = result["reason"]

    if decision == "ACCEPT":
        print("Candidate Accepted")
        print("Action: Schedule Interview")

    elif decision == "REJECT":
        print("Candidate Rejected")
        print("Action: Send Rejection Email")

    else:
        print("Candidate Needs Human Review")
        print("Action: Forward to Recruiter")

    print(f"Reason: {reason}")

import json
import os
import time
from config import llm
from prompts import REACT_PROMPT

# ==========================
# Paths
# ==========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

CANDIDATES_FOLDER = os.path.join(PROJECT_ROOT, "test_data", "candidates")
HISTORY_FOLDER = os.path.join(PROJECT_ROOT, "test_data", "history")
JOBS_FOLDER = os.path.join(PROJECT_ROOT, "test_data", "jobs")


# ==========================
# Helpers
# ==========================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_jobs():
    jobs = []

    for file in sorted(os.listdir(JOBS_FOLDER)):
        if file.endswith(".json"):
            jobs.append(
                load_json(
                    os.path.join(JOBS_FOLDER, file)
                )
            )

    return jobs


# ==========================
# LLM Evaluation
# ==========================

def evaluate_candidate(candidate, job, history):

    prompt = f"""
{REACT_PROMPT}

Candidate:
{json.dumps(candidate, indent=2)}

Job:
{json.dumps(job, indent=2)}

Application History:
{json.dumps(history, indent=2)}

Evaluate ONLY this job.

Return exactly in this format:

Reasoning:
...

Match Score: <0-100>

Decision:
ACCEPT
or
REJECT
or
IDLE
"""
    

    start = time.time()
    response = llm.invoke(prompt)
    print(response.response_metadata)

    return response.content
    end = time.time()

    print(
        "Latency:",
        end-start
    )


# ==========================
# Main
# ==========================

def main():

    jobs = load_all_jobs()

    for file in sorted(os.listdir(CANDIDATES_FOLDER)):

        if not file.endswith(".json"):
            continue

        candidate = load_json(
            os.path.join(CANDIDATES_FOLDER, file)
        )

        # Load Candidate History
        history_file = os.path.join(
            HISTORY_FOLDER,
            f"history_{candidate['id']}.json"
        )

        if os.path.exists(history_file):
            history = load_json(history_file)
        else:
            history = {
                "previous_applications": []
            }

        best_score = -1
        best_result = None
        best_job = None

        print("\n" + "=" * 70)
        print(f"Evaluating Candidate: {candidate['name']}")
        print("=" * 70)

        for job in jobs:

            print(f"\nChecking Job: {job['job']['title']}")

            result = evaluate_candidate(
                candidate,
                job,
                history
            )

            print(result)

            # Extract Match Score
            try:

                score_line = next(
                    line for line in result.splitlines()
                    if "Match Score" in line
                )

                score = int(
                    score_line.split(":")[1].strip()
                )

            except Exception:
                score = 0

            if score > best_score:
                best_score = score
                best_result = result
                best_job = job

        print("\n" + "=" * 70)
        print("FINAL RESULT")
        print("=" * 70)

        print(f"Candidate : {candidate['name']}")
        print(f"Best Job  : {best_job['job']['title']}")
        print(f"Score     : {best_score}")

        print("\nLLM Decision:\n")
        print(best_result)

        print("=" * 70)


if __name__ == "__main__":
    main()
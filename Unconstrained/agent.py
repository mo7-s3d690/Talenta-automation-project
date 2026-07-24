import json
import os

from config import client
from prompts import REACT_PROMPT

CANDIDATES_FOLDER = "../test_data/candidates"
HISTORY_FOLDER = "../test_data/history"
JOB_FILE = "../test_data/job.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_candidate(candidate, job, history):

    prompt = f"""
{REACT_PROMPT}

Candidate:
{candidate}

Job Requirements:
{job}

Application History:
{history}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


def main():

    job = load_json(JOB_FILE)

    for filename in sorted(os.listdir(CANDIDATES_FOLDER)):

        if not filename.endswith(".json"):
            continue

        candidate_path = os.path.join(CANDIDATES_FOLDER, filename)
        candidate = load_json(candidate_path)

        history_path = os.path.join(
            HISTORY_FOLDER,
            f"history_{candidate['id']}.json"
        )

        if os.path.exists(history_path):
            history = load_json(history_path)
        else:
            history = {
                "previous_applications": []
            }

        print("=" * 60)
        print(f"Candidate: {candidate['name']}")

        result = evaluate_candidate(candidate, job, history)

        print(result)

        print("=" * 60)


if __name__ == "__main__":
    main()
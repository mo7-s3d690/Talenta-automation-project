import os

from config import (
    CANDIDATES_FOLDER,
    HISTORY_FOLDER,
    JOB_FILE
)

from utils import load_json
from rules import evaluate_candidate
from actions import execute_action


def main():

    job = load_json(JOB_FILE)["job"]

    for filename in sorted(os.listdir(CANDIDATES_FOLDER)):

        if not filename.endswith(".json"):
            continue

        candidate = load_json(
            os.path.join(CANDIDATES_FOLDER, filename)
        )

        history_path = os.path.join(
            HISTORY_FOLDER,
            f"history_{candidate['id']}.json"
        )

        if os.path.exists(history_path):
            history = load_json(history_path)
        else:
            history = {}

        print("=" * 60)
        print(f"Candidate: {candidate['name']}")

        result = evaluate_candidate(
            candidate,
            job,
            history
        )

        execute_action(result)

        print("=" * 60)


if __name__ == "__main__":
    main()
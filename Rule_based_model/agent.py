import os

import time
from utils import (
    load_json,
    load_all_jobs
)

from rules import evaluate_rules

from actions import print_result



BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


PROJECT_ROOT = os.path.dirname(
    BASE_DIR
)



CANDIDATES_FOLDER = os.path.join(
    PROJECT_ROOT,
    "test_data",
    "candidates"
)


JOBS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "test_data",
    "jobs"
)




def main():
    
    start = time.time()
    jobs = load_all_jobs(
        JOBS_FOLDER
    )


    for file in sorted(
        os.listdir(CANDIDATES_FOLDER)
    ):


        if not file.endswith(".json"):

            continue



        candidate = load_json(
            os.path.join(
                CANDIDATES_FOLDER,
                file
            )
        )



        best_job = None

        best_result = None



        for job in jobs:


            result = evaluate_rules(
                candidate,
                job
            )



            if (
                best_result is None
                or
                result["score"]
                >
                best_result["score"]

            ):

                best_result = result

                best_job = job




        print_result(
            candidate,
            best_job,
            best_result
        )
    end = time.time()

    print(
        "Latency:",
        end-start,
        "seconds"
    )




if __name__ == "__main__":

    main()
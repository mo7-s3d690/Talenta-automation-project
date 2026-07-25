import json
import os



def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)



def load_all_jobs(folder):

    jobs = []

    for file in sorted(os.listdir(folder)):

        if file.endswith(".json"):

            job_path = os.path.join(
                folder,
                file
            )

            jobs.append(
                load_json(job_path)
            )

    return jobs
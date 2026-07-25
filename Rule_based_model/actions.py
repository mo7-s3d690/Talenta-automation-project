def print_result(candidate, job, result):

    print("=" * 60)

    print(
        f"Candidate: {candidate['name']}"
    )

    print(
        f"Best Match Job: {job['job']['title']}"
    )

    print(
        f"Match Score: {result['score']}"
    )

    print(
        f"Decision: {result['decision']}"
    )


    print(
        "Details:"
    )

    print(
        f"- Experience Score: {result['experience_score']}"
    )

    print(
        f"- Education Score: {result['education_score']}"
    )

    print(
        f"- Skills Score: {result['skill_score']}"
    )


    print("=" * 60)
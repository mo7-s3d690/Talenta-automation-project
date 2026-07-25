def extract_work_history(candidate):
    return candidate.get("experience", [])


def extract_skills(candidate):
    return candidate.get("skills", [])


def extract_education(candidate):
    return candidate.get("education", [])


def extract_history(history):
    return history.get("previous_applications", [])
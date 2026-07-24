import json


def load_json(file_path):
    """Load JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def count_matching_skills(candidate_skills, required_skills):
    """
    Count how many required skills are found in the candidate skills.
    """

    candidate = {skill.lower() for skill in candidate_skills}
    required = {skill.lower() for skill in required_skills}

    return len(candidate & required)


def degree_matches(candidate_education, required_degrees):
    """
    Check if candidate has one of the required degrees.
    """

    required = [d.lower() for d in required_degrees]

    for edu in candidate_education:
        degree = edu.get("degree", "").lower()

        for req in required:
            if req in degree:
                return True

    return False

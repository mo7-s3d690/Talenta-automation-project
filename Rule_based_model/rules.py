from config import MIN_EXPERIENCE_GAP
from utils import count_matching_skills, degree_matches


def evaluate_candidate(candidate, job, history):

    experience = candidate.get("experience_years", 0)
    skills = candidate.get("skills", [])
    education = candidate.get("education", [])

    required_skills = job["required_skills"]
    required_degree = job["required_degree"]

    matched_skills = count_matching_skills(
        skills,
        required_skills
    )

    required_skill_count = job["minimum_required_skills"]
    required_experience = job["minimum_experience"]

    # ---------- Rule 1 ----------
    if not skills or experience is None:
        return {
            "decision": "IDLE",
            "reason": "Missing important candidate information."
        }

    # ---------- Rule 2 ----------
    if history.get("current_status") == "INTERVIEW":
        return {
            "decision": "IDLE",
            "reason": "Candidate already in hiring pipeline."
        }

    # ---------- Rule 3 ----------
    if experience < required_experience - MIN_EXPERIENCE_GAP:
        return {
            "decision": "REJECT",
            "reason": "Experience below minimum requirement."
        }

    # ---------- Rule 4 ----------
    if matched_skills < required_skill_count:
        return {
            "decision": "REJECT",
            "reason": "Insufficient required skills."
        }

    # ---------- Rule 5 ----------
    if not degree_matches(education, required_degree):
        return {
            "decision": "IDLE",
            "reason": "Degree requires recruiter review."
        }

    # ---------- Rule 6 ----------
    return {
        "decision": "ACCEPT",
        "reason": "Candidate satisfies all requirements."
    }

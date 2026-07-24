import json
import os
from config import JOB_SPEC, TEST_DATA_DIR

_APPLICATION_HISTORY = {
    f"candidate_{i}": {"previously_rejected_for_similar_role": False, "already_in_pipeline_elsewhere": False}
    for i in range(1, 9)
}


def _load_candidate(candidate_id: str):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    candidates_dir = os.path.join(base_dir, "test_data", "candidates")

    print(f"🔍 Searching in: {candidates_dir}")

    for fname in os.listdir(candidates_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(candidates_dir, fname)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

            file_id = fname.replace(".json", "").replace("candidate_", "")
            if (data.get("id") == candidate_id or
                    data.get("candidate_id") == candidate_id or
                    fname.startswith(candidate_id) or
                    file_id == candidate_id.replace("candidate_", "")):
                print(f"✅ Loaded: {fname} → {data.get('name', 'Unknown')}")
                return data
        except:
            continue

    raise ValueError(f"❌ Candidate '{candidate_id}' not found.")


def check_qualifications(candidate_id: str):
    c = _load_candidate(candidate_id)
    years = c.get("experience_years", 0)
    degrees = [e.get("degree", "").lower() for e in c.get("education", [])]
    degree_match = any(field in " ".join(degrees) for field in JOB_SPEC["required_degree_fields"])
    return {
        "years_experience": years,
        "meets_min_experience": years >= JOB_SPEC["min_years_experience"],
        "degree_field_match": degree_match,
    }


def check_skill_coverage(candidate_id: str):
    c = _load_candidate(candidate_id)
    text = " ".join(c.get("skills", [])).lower()
    for exp in c.get("experience", []):
        text += " " + " ".join(exp.get("responsibilities", [])).lower()
    covered = [skill for skill in JOB_SPEC["core_skill_areas"] if skill.lower() in text]
    return {
        "covered": covered,
        "coverage_ratio": round(len(covered) / len(JOB_SPEC["core_skill_areas"]), 2) if JOB_SPEC[
            "core_skill_areas"] else 0
    }


def check_application_history(candidate_id: str):
    key = f"candidate_{candidate_id.split('_')[-1]}" if '_' in candidate_id else candidate_id
    return _APPLICATION_HISTORY.get(key, {"previously_rejected_for_similar_role": False,
                                          "already_in_pipeline_elsewhere": False})


TOOL_REGISTRY = {
    "check_qualifications": check_qualifications,
    "check_skill_coverage": check_skill_coverage,
    "check_application_history": check_application_history,
}
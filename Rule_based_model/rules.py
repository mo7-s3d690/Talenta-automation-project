SKILL_MAPPING = {

    # =====================
    # Software Development
    # =====================

    "react": [
        "front-end development"
    ],

    "angular": [
        "front-end development"
    ],

    "vue": [
        "front-end development"
    ],


    "node": [
        "back-end development"
    ],

    "node.js": [
        "back-end development"
    ],

    "django": [
        "back-end development"
    ],

    "flask": [
        "back-end development"
    ],


    "api": [
        "RESTful API design"
    ],

    "rest": [
        "RESTful API design"
    ],


    "sql": [
        "database design (SQL/NoSQL)"
    ],

    "mysql": [
        "database design (SQL/NoSQL)"
    ],

    "mongodb": [
        "database design (SQL/NoSQL)"
    ],


    "git": [
        "version control (Git)"
    ],


    "docker": [
        "CI/CD & deployment"
    ],



    # =====================
    # Finance
    # =====================

    "accounting": [
        "financial reporting & statements"
    ],

    "financial reporting": [
        "financial reporting & statements"
    ],

    "budget": [
        "budgeting & forecasting"
    ],

    "forecast": [
        "budgeting & forecasting"
    ],

    "erp": [
        "ERP / finance systems"
    ],

    "sap": [
        "ERP / finance systems"
    ],

    "audit": [
        "audit coordination"
    ],

    "tax": [
        "tax & regulatory compliance"
    ],



    # =====================
    # HR
    # =====================

    "recruitment": [
        "recruitment & sourcing"
    ],

    "sourcing": [
        "recruitment & sourcing"
    ],

    "payroll": [
        "payroll management"
    ],

    "attendance": [
        "time & attendance tracking"
    ],

    "training": [
        "training needs analysis"
    ]

}



def normalize(text):

    return text.lower().strip()



def extract_candidate_text(candidate):

    data = []


    for skill in candidate.get("skills", []):

        data.append(
            normalize(skill)
        )


    for exp in candidate.get("experience", []):

        for responsibility in exp.get(
            "responsibilities",
            []
        ):

            data.append(
                normalize(responsibility)
            )


    return data




def calculate_skill_score(candidate, job):

    candidate_text = extract_candidate_text(candidate)


    required_skills = (
        job["job"]
        ["structured_fields"]
        ["core_skill_areas"]
    )


    matched = set()


    for text in candidate_text:

        for keyword, categories in SKILL_MAPPING.items():

            if keyword in text:

                for category in categories:

                    matched.add(
                        category.lower()
                    )


    count = 0


    for skill in required_skills:

        if skill.lower() in matched:

            count += 1



    if len(required_skills) == 0:

        return 0


    return int(
        (count / len(required_skills))
        * 100
    )




def calculate_experience_score(candidate, job):

    candidate_exp = candidate.get(
        "experience_years",
        0
    )


    required_exp = (
        job["job"]
        ["structured_fields"]
        ["min_years_experience"]
    )


    if candidate_exp >= required_exp:

        return 100


    return int(
        (candidate_exp / required_exp)
        * 100
    )




def calculate_education_score(candidate, job):

    required_fields = (
        job["job"]
        ["structured_fields"]
        ["required_degree_fields"]
    )


    for education in candidate.get(
        "education",
        []
    ):

        degree = education["degree"].lower()


        for field in required_fields:

            if field.lower() in degree:

                return 100


    return 0




def evaluate_rules(candidate, job):


    experience_score = calculate_experience_score(
        candidate,
        job
    )


    education_score = calculate_education_score(
        candidate,
        job
    )


    skill_score = calculate_skill_score(
        candidate,
        job
    )



    final_score = int(

        experience_score * 0.4 +

        education_score * 0.2 +

        skill_score * 0.4

    )



    if final_score >= 70:

        decision = "ACCEPT"


    elif final_score >= 40:

        decision = "IDLE"


    else:

        decision = "REJECT"



    return {

        "score": final_score,

        "decision": decision,

        "experience_score": experience_score,

        "education_score": education_score,

        "skill_score": skill_score

    }
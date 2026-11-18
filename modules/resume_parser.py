import re


# --------------------------------------------------
# SKILLS DATABASE
# --------------------------------------------------

SKILLS = [

    # Programming Languages
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "php",
    "ruby",
    "go",

    # Web Development
    "html",
    "css",
    "react",
    "angular",
    "node.js",
    "nodejs",
    "express",
    "django",
    "flask",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "oracle",
    "sqlite",

    # AI / ML / Data
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "natural language processing",
    "data science",
    "data analysis",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "opencv",

    # Cloud / DevOps
    "aws",
    "azure",
    "google cloud",
    "docker",
    "kubernetes",
    "linux",

    # Tools
    "git",
    "github",
    "gitlab",

    # Other
    "power bi",
    "tableau",
    "excel"
]


# --------------------------------------------------
# CLEAN TEXT
# --------------------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# --------------------------------------------------
# EXTRACT SKILLS
# --------------------------------------------------

def extract_skills(text):

    text = clean_text(text)

    found_skills = []

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill.lower())
            + r"(?!\w)"
        )

        if re.search(pattern, text):

            found_skills.append(skill)

    return sorted(
        set(found_skills)
    )


# --------------------------------------------------
# COMPARE SKILLS
# --------------------------------------------------

def compare_skills(
    required_skills,
    candidate_skills
):

    required = set(
        skill.lower()
        for skill in required_skills
    )

    candidate = set(
        skill.lower()
        for skill in candidate_skills
    )

    # Skills present in both
    matched_skills = sorted(
        required.intersection(candidate)
    )

    # Required skills absent from resume
    missing_skills = sorted(
        required - candidate
    )

    # Calculate percentage
    if required:

        skill_score = (
            len(matched_skills)
            / len(required)
        ) * 100

    else:

        skill_score = 0

    return (
        matched_skills,
        missing_skills,
        round(skill_score, 2)
    )
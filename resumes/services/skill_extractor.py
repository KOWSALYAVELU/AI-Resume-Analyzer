import re
 
SKILL_ALIASES = {
    # Developer
    "python": ["python"],
    "django": ["django"],
    "django rest framework": ["django rest framework", "drf"],
    "rest api": ["rest api", "restful api", "restful apis"],
    "mysql": ["mysql"],
    "sqlite": ["sqlite", "sqlite3"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "javascript": ["javascript", "js"],
    "git": ["git"],
    "github": ["github"],

    # Testing / QA
    "software testing": ["testing", "qa", "quality assurance"],
    "selenium": ["selenium", "automation testing"],

    # DevOps
    "devops": ["devops", "ci/cd", "jenkins"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],

    # Cloud
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "gcp": ["gcp", "google cloud"],

    # Data / Analytics
    "postgresql": ["postgresql", "postgres"],
    "big data": ["big data", "hadoop", "spark"],
    "etl": ["etl", "data pipeline"],

    # AI / ML
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "tensorflow", "pytorch"],
    "natural language processing": ["natural language processing", "nlp"],

    # Security
    "cybersecurity": ["cybersecurity", "network security", "ethical hacking"]
}


def extract_skills(text):
    normalized_text = text.lower()
    found_skills = []

    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = (
                r"(?<!\w)"
                + re.escape(alias.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, normalized_text):
                found_skills.append(canonical_skill)
                break

    return found_skills  
        
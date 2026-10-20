import re


SECTION_KEYWORDS = {
    "education": ["education", "academic qualification"],
    "skills": ["skills", "technical skills", "technical stack"],
    "projects": ["projects", "personal projects", "academic projects"],
    "experience": ["experience", "work experience", "internship", "work history"],
    "summary": ["summary", "profile", "objective", "about me"],
}

ACTION_VERBS = [
    "developed", "built", "created", "implemented", "designed",
    "improved", "analyzed", "optimized", "led", "managed",
    "collaborated", "contributed", "engineered", "deployed",
    "tested", "debugged", "documented", "researched", "automated",
    "streamlined", "mentored", "trained", "evaluated", "integrated",
]

# order of importance for each section, out of 100
WEIGHTS = {
    "contact_details": 8,
    "phone": 4,
    "links": 5,
    "summary": 5,
    "education": 10,
    "skills": 12,
    "projects": 12,
    "experience": 10,
    "action_verbs": 10,
    "bullets": 6,
    "metrics": 8,
    "readability": 10,
}

# Advice for each section, if missing
ADVICE = {
    "contact_details": "Add a professional email address.",
    "phone": "Add a phone number so recruiters can reach you.",
    "links": "Add your GitHub or LinkedIn profile link.",
    "summary": "Add a short summary section at the top.",
    "education": "Add a clearly labeled Education section.",
    "skills": "Add a clearly labeled Skills section.",
    "projects": "Add a Projects section with what you built.",
    "experience": "Add an Experience or Internship section (if you have one).",
    "action_verbs": "Start bullet points with action verbs such as built, developed or designed.",
    "bullets": "Use bullet points to describe your projects and work.",
    "metrics": "Add numbers where true (for example: 30% faster, 5 endpoints).",
    "readability": "Keep the resume between about 150 and 900 words.",
}


def _heading_lines(text):
    """Extract heading lines (section titles) from the text."""
    return [
        line.strip().lower()
        for line in text.splitlines()
        if 0 < len(line.strip()) <= 50
    ]


def _has_section(headings, keywords):
    return any(
        keyword in heading
        for heading in headings
        for keyword in keywords
    )


def score_resume(text):
    normalized_text = text.lower()
    headings = _heading_lines(text)
    word_count = len(text.split())

    distinct_verbs = {
        verb for verb in ACTION_VERBS
        if re.search(rf"\b{verb}\b", normalized_text)
    }

    bullet_lines = [
        line for line in text.splitlines()
        if re.match(r"^\s*[•\-\*–▪●]\s+\S", line)
    ]

    metric_matches = re.findall(
        r"\d+(?:\.\d+)?\s?(?:%|\+|x\b|k\b)",
        normalized_text,
    )

    checks = {
        "contact_details": bool(
            re.search(
                r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
                text,
                re.IGNORECASE,
            )
        ),
        "phone": bool(re.search(r"(?:\+?\d[\s-]?){10,13}", text)),
        "links": bool(
            re.search(r"github|linkedin", normalized_text)
        ),
        "summary": _has_section(headings, SECTION_KEYWORDS["summary"]),
        "education": _has_section(headings, SECTION_KEYWORDS["education"]),
        "skills": _has_section(headings, SECTION_KEYWORDS["skills"]),
        "projects": _has_section(headings, SECTION_KEYWORDS["projects"]),
        "experience": _has_section(headings, SECTION_KEYWORDS["experience"]),
        "action_verbs": len(distinct_verbs) >= 4,
        "bullets": len(bullet_lines) >= 5,
        "metrics": len(metric_matches) >= 1,
        "readability": 150 <= word_count <= 900,
    }

    score = sum(
        WEIGHTS[name]
        for name, passed in checks.items()
        if passed
    )

    suggestions = [
        ADVICE[name]
        for name, passed in checks.items()
        if not passed
    ]

    return {
        "score": score,
        "checks": checks,
        "suggestions": suggestions,
    }
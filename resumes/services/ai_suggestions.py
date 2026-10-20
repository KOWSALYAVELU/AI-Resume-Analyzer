def generate_suggestions(
    resume_score,
    resume_skills,
    missing_skills,
    score_suggestions,
):
    suggestions = list(score_suggestions)

    if not resume_skills:
        suggestions.append(
            "Add a clearly labeled technical skills section."
        )

    if missing_skills:
        suggestions.append(
            "Review these job requirements: "
            + ", ".join(missing_skills)
            + ". Add them only if you genuinely have those skills."
        )

    if resume_score < 50:
        suggestions.append(
            "Review your resume structure and make sure "
            "your education, skills, and projects are clearly described."
        )

    return suggestions
from .skill_extractor import extract_skills
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_similarity(resume_text, job_description):
    """
    Calculate text similarity between a resume and a job description.
    """

    if not resume_text.strip() or not job_description.strip():
        return 0.0

    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    try:
        vectors = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        return 0.0

def match_resume_to_job(resume_text, job_description):
    # Step 1: Extract skills from resume
    resume_skills = set(
        extract_skills(resume_text)
    )

    # Step 2: Extract required skills from job description
    job_skills = set(
        extract_skills(job_description)
    )

    # Step 3: Find matching skills
    matched_skills = sorted(
        resume_skills & job_skills
    )

    # Step 4: Find missing skills
    missing_skills = sorted(
        job_skills - resume_skills
    )

    # Step 5: Calculate skill match score
    if job_skills:
        skill_match_score = round(
            len(matched_skills) / len(job_skills) * 100,
            2
        )
    else:
        skill_match_score = 0.0

    # Step 6: Calculate NLP similarity
    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )

    # Step 7: Return all results
    return {
        "match_score": skill_match_score,
        "similarity_score": similarity_score,
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(job_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
    }
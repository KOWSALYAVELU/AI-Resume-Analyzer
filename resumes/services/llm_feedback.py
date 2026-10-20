import json
import os

from google import genai


def get_llm_feedback(resume_text, job_description, missing_skills):
    """
    LLM resume get feedback.

    """

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = f"""You are a career coach reviewing a resume for a job.

JOB DESCRIPTION:
{job_description[:3000]}

RESUME:
{resume_text[:6000]}

Skills the job needs that were not detected in the resume:
{", ".join(missing_skills) or "none"}

Give exactly 4 short, specific, actionable suggestions to improve this
resume for this job. Never suggest claiming skills the candidate does
not have. Reply ONLY with a JSON list of 4 strings, nothing else."""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)

    except Exception as error:
        print("LLM ERROR:", repr(error))
        return None
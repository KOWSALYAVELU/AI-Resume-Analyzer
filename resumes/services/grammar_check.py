import json
import os

from google import genai


def check_grammar(resume_text):
    """
    Finds grammar, spelling, and writing errors in a resume.
    Each error contains: {"issue": "...", "fix": "..."}.
    Returns None if an error occurs, so the app does not crash.
    """

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = f"""You are a proofreader for resumes.

Find ONLY real grammar, spelling, punctuation, tense-consistency and
repeated-word mistakes in the resume below.

RULES:
- Ignore names of technologies, companies, people and URLs
  (for example Django, ShopKart, MySQL, GitHub).
- Do not give style opinions or content advice.
- Report at most 6 mistakes.
- If there are no mistakes, return an empty list [].
- Reply ONLY with a JSON list. Each item must be an object with two keys:
  "issue" (the exact text that is wrong, with a short reason) and
  "fix" (the corrected text).

RESUME:
{resume_text[:6000]}
"""

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt,
        )

        text = response.text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        data = json.loads(text)

        # Safety check: Keep only items with the correct structure.
        return [
            {"issue": str(item["issue"]), "fix": str(item["fix"])}
            for item in data
            if isinstance(item, dict) and "issue" in item and "fix" in item
        ]

    except Exception as error:
        print("GRAMMAR ERROR:", repr(error))
        return None
    

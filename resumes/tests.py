from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import ResumeAnalysis
from .services.ai_suggestions import generate_suggestions
from .services.job_matcher import match_resume_to_job
from .services.resume_scorer import score_resume
from .services.skill_extractor import extract_skills


class SkillExtractorTests(TestCase):

    def test_detects_multiple_skills(self):
        text = "I know Python, Django and MySQL."
        skills = extract_skills(text)

        self.assertIn("python", skills)
        self.assertIn("django", skills)
        self.assertIn("mysql", skills)

    def test_detects_alias(self):
        skills = extract_skills("Worked with k8s and DRF")

        self.assertIn("kubernetes", skills)
        self.assertIn("django rest framework", skills)

    def test_no_skills_in_unrelated_text(self):
        self.assertEqual(extract_skills("I like cooking and music."), [])

    def test_does_not_match_inside_words(self):
        # "git" should not match inside "digital"
        self.assertNotIn("git", extract_skills("digital marketing"))


class ResumeScorerTests(TestCase):

    def test_empty_text_scores_zero(self):
        result = score_resume("")
        self.assertEqual(result["score"], 0)

    def test_email_is_detected(self):
        result = score_resume("Contact: student@example.com")
        self.assertTrue(result["checks"]["contact_details"])

    def test_score_is_between_0_and_100(self):
        result = score_resume(
            "Education Skills Projects Experience developed " * 30
        )
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_missing_sections_create_suggestions(self):
        result = score_resume("Hello")
        self.assertTrue(len(result["suggestions"]) > 0)

    def test_full_resume_scores_high(self):
        text = """
        Jane Doe
        jane@example.com | +91 98765 43210 | github.com/jane
        PROFILE SUMMARY
        Python developer.
        EDUCATION
        BCA 2022-2025
        SKILLS
        Python, Django
        PROJECTS
        - Built a shop backend with Django
        - Developed REST APIs for products
        - Designed a database schema
        - Implemented cart and checkout
        - Tested 20+ endpoints with 100% pass rate
        EXPERIENCE
        Internship at ABC Company
        """ + ("word " * 150)
        result = score_resume(text)
        self.assertGreaterEqual(result["score"], 85)

    def test_section_word_in_sentence_does_not_count(self):
        # "skills" in a sentence should not count as a skills section.
        text = "I have good communication skills and enjoy teamwork " * 5
        self.assertFalse(score_resume(text)["checks"]["skills"])

    def test_section_word_in_sentence_does_not_count(self):
        # "skills" in a sentence should not count as a skills section.
        text = "I have good communication skills and enjoy teamwork " * 5
        self.assertFalse(score_resume(text)["checks"]["skills"])    


class JobMatcherTests(TestCase):

    def test_matched_and_missing_skills(self):
        resume = "Python and Django developer"
        job = "Need Python, Django and Docker experience"

        result = match_resume_to_job(resume, job)

        self.assertIn("python", result["matched_skills"])
        self.assertIn("django", result["matched_skills"])
        self.assertIn("docker", result["missing_skills"])

    def test_match_score_calculation(self):
        resume = "Python"
        job = "Python and Docker"

        result = match_resume_to_job(resume, job)

        self.assertEqual(result["match_score"], 50.0)

    def test_empty_job_description_gives_zero(self):
        result = match_resume_to_job("Python developer", "")
        self.assertEqual(result["match_score"], 0.0)


class SuggestionTests(TestCase):

    def test_missing_skills_are_mentioned(self):
        suggestions = generate_suggestions(80, ["python"], ["docker"], [])
        self.assertTrue(any("docker" in s for s in suggestions))

    def test_low_score_adds_structure_advice(self):
        suggestions = generate_suggestions(30, ["python"], [], [])
        self.assertTrue(len(suggestions) >= 1)


class ViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", password="StrongPass123"
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_analyzer_page_loads(self):
        response = self.client.get(reverse("analyze_resume"))
        self.assertEqual(response.status_code, 200)

    def test_history_requires_login(self):
        response = self.client.get(reverse("history"))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_history_shows_only_own_analyses(self):
        other = User.objects.create_user(username="other", password="StrongPass123")

        ResumeAnalysis.objects.create(
            user=self.user, resume_name="mine.pdf", job_description="x",
            resume_score=80, match_score=50.0,
        )
        ResumeAnalysis.objects.create(
            user=other, resume_name="theirs.pdf", job_description="x",
            resume_score=60, match_score=40.0,
        )

        self.client.login(username="tester", password="StrongPass123")
        response = self.client.get(reverse("history"))

        self.assertContains(response, "mine.pdf")
        self.assertNotContains(response, "theirs.pdf")

    def test_register_creates_user(self):
        response = self.client.post(reverse("register"), {
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())
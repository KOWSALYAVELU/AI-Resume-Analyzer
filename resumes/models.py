from django.conf import settings
from django.db import models


class ResumeAnalysis(models.Model):
    """Stores the result of one resume analysis."""

    # Who ran the analysis (optional, because login is not built yet)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="analyses",
    )

    # Basic information
    resume_name = models.CharField(max_length=255)
    job_description = models.TextField()

    # Scores
    resume_score = models.PositiveIntegerField()
    match_score = models.FloatField()

    # Lists of skills and suggestions (stored as JSON lists)
    detected_skills = models.JSONField(default=list)
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    suggestions = models.JSONField(default=list)

    # Set automatically when the record is created
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # newest first

    def __str__(self):
        return f"{self.resume_name} - {self.resume_score}/100"
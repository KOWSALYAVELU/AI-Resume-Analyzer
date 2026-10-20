from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label="Upload your resume",
        help_text="Supported formats: PDF and DOCX"
    )

    job_description = forms.CharField(
        label="Job description",
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": (
                    "Paste the job description here..."
                ),
            }
        ),
        required=True,
    )

    def clean_resume(self):
        uploaded_file = self.cleaned_data["resume"]

        allowed_extensions = {".pdf", ".docx"}

        filename = uploaded_file.name.lower()
        extension = "." + filename.rsplit(".", 1)[-1]

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Please upload a PDF or DOCX file."
            )

        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                "File size must be 5 MB or less."
            )

        return uploaded_file

    def clean_job_description(self):
        description = self.cleaned_data[
            "job_description"
        ].strip()

        if len(description) < 20:
            raise forms.ValidationError(
                "Please enter a more detailed job description."
            )

        return description
    
    from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ResumeUploadForm(forms.Form):
    resume = forms.FileField(
        label="Upload your resume",
        help_text="Supported formats: PDF and DOCX"
    )

    job_description = forms.CharField(
        label="Job description",
        widget=forms.Textarea(
            attrs={
                "rows": 8,
                "placeholder": (
                    "Paste the job description here..."
                ),
            }
        ),
        required=True,
    )

    def clean_resume(self):
        uploaded_file = self.cleaned_data["resume"]

        allowed_extensions = {".pdf", ".docx"}

        filename = uploaded_file.name.lower()
        extension = "." + filename.rsplit(".", 1)[-1]

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Please upload a PDF or DOCX file."
            )

        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:
            raise forms.ValidationError(
                "File size must be 5 MB or less."
            )

        return uploaded_file

    def clean_job_description(self):
        description = self.cleaned_data[
            "job_description"
        ].strip()

        if len(description) < 20:
            raise forms.ValidationError(
                "Please enter a more detailed job description."
            )

        return description

class RegisterForm(UserCreationForm):
        email = forms.EmailField(required=True)

        class Meta:
            model = User
            fields = ("username", "email", "password1", "password2")
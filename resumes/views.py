from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


from django.http import HttpResponse
from .services.resume_rewriter import build_docx, rewrite_resume
from .forms import RegisterForm, ResumeUploadForm
from .models import ResumeAnalysis
from .services.ai_suggestions import generate_suggestions
from .services.job_matcher import match_resume_to_job
from .services.resume_parser import extract_resume_text
from .services.resume_scorer import score_resume
from .services.skill_extractor import extract_skills
from .services.llm_feedback import get_llm_feedback
from .services.grammar_check import check_grammar


def home(request):
    return render(request, "resumes/home.html")


def analyze_resume(request):
    result = None

    if request.method == "POST":
        form = ResumeUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = form.cleaned_data["resume"]
            job_description = form.cleaned_data[
                "job_description"
            ]
            try:
                extracted_text = extract_resume_text(uploaded_file)

                if not extracted_text:
                    form.add_error(
                        "resume",
                        "No readable text was found in the resume."
                    )

                else:
                    skills = extract_skills(extracted_text)

                    resume_analysis = score_resume(
                        extracted_text
                    )

                    job_match = match_resume_to_job(
                        extracted_text,
                        job_description,
                    )

                    suggestions = generate_suggestions(
                        resume_analysis["score"],
                        skills,
                        job_match["missing_skills"],
                        resume_analysis["suggestions"],
                    )
                    llm_feedback = get_llm_feedback(
                        extracted_text,
                        job_description,
                        job_match["missing_skills"],
                    )

                    grammar_issues = check_grammar(extracted_text)

                    result = {
                        "resume_score": resume_analysis["score"],
                        "skills": skills,
                        "checks": resume_analysis["checks"],
                        "suggestions": suggestions,
                        "job_match": job_match,
                        "llm_feedback": llm_feedback,
                        "grammar_issues": grammar_issues,
                    }   
                    ResumeAnalysis.objects.create(
                        user=request.user if request.user.is_authenticated else None,
                        resume_name=uploaded_file.name,
                        job_description=job_description,
                        resume_score=resume_analysis["score"],
                        match_score=job_match["match_score"],
                        detected_skills=skills,
                        matched_skills=job_match["matched_skills"],
                        missing_skills=job_match["missing_skills"],
                        suggestions=suggestions,
                    )


            except Exception as error:
                print("ANALYZE ERROR:", repr(error))
                form.add_error(
                    "resume",
                    "We could not read this file. "
                    "Please upload a valid PDF or DOCX document."
                )

    else:
        form = ResumeUploadForm()

    return render(
        request,
        "resumes/analyzer.html",
        {
            "form": form,
            "result": result,
        },
    )


@login_required
def history(request):
    analyses = ResumeAnalysis.objects.filter(user=request.user)
    return render(request, "resumes/history.html", {"analyses": analyses})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)      # register after go to login
            return redirect("analyze_resume")
    else:
        form = RegisterForm()

    return render(request, "resumes/register.html", {"form": form})


@login_required
def improved_resume(request):
    if request.method != "POST":
        return redirect("analyze_resume")

    form = ResumeUploadForm(request.POST, request.FILES)

    if not form.is_valid():
        return render(
            request,
            "resumes/analyzer.html",
            {"form": form, "result": None},
        )

    try:
        text = extract_resume_text(form.cleaned_data["resume"])
    except Exception:
        text = ""

    improved = rewrite_resume(text, form.cleaned_data["job_description"]) if text else None

    if not improved:
        form.add_error(
            None,
            "Could not generate the improved resume right now. Please try again later.",
        )
        return render(
            request,
            "resumes/analyzer.html",
            {"form": form, "result": None},
        )

    response = HttpResponse(
        build_docx(improved),
        content_type=(
            "application/vnd.openxmlformats-officedocument"
            ".wordprocessingml.document"
        ),
    )
    response["Content-Disposition"] = 'attachment; filename="improved_resume.docx"'
    return response
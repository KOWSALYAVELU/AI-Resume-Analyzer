from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("analyzer/", views.analyze_resume, name="analyze_resume"),
    path("history/", views.history, name="history"),
    path("register/", views.register, name="register"),
    path("login/",auth_views.LoginView.as_view(template_name="resumes/login.html"),name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("improved-resume/", views.improved_resume, name="improved_resume"),
]
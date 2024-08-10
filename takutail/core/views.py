# from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView


class LoginView(LoginView):
    template_name = "core/login.html"


class LogoutView(LogoutView):
    pass

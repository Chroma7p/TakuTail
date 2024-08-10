from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, CreateView
from django.shortcuts import render, redirect
from .forms import SignUpForm
from users.models import CustomUser


# def signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("home")  # サインアップ後にリダイレクトするURL
#     else:
#         form = SignUpForm()
#     return render(request, "signup.html", {"form": form})

def root_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return redirect('login')


class SignUpView(CreateView):
    model = CustomUser
    template_name = "signup.html"
    form_class = SignUpForm
    success_url = "/home/"

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class LoginView(LoginView):
    template_name = "login.html"


class LogoutView(LogoutView):
    pass


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

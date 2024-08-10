from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    # path("login/", include("allauth.urls")),
    # path("accounts/", include("allauth.urls")),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("login/", views.LoginView.as_view(), name="login"),
    path("login/", include("allauth.urls")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls"), name="core"),
    path("cocktails/", include("cocktails.urls"),name='cocktails'),
    path("ingredients/", include("ingredients.urls"),name='ingredients'),
    path("users/", include("users.urls"),name='users'),
]

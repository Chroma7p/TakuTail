# myproject/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('cocktails/', include('cocktails.urls')),
    path('ingredients/', include('ingredients.urls')),
    path('users/', include('users.urls')),
]

# ingredients/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sakes', views.SakeViewSet)
router.register(r'waris', views.WariViewSet)
router.register(r'others', views.OtherViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

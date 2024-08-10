from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'user_sakes', views.UserSakeViewSet)
router.register(r'user_waris', views.UserWariViewSet)
router.register(r'user_others', views.UserOtherViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

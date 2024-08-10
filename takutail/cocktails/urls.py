from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cocktails', views.CocktailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_random_cocktail/', views.create_random_cocktail, name='create_random_cocktail'),
]

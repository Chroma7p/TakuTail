from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cocktails', views.CocktailViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_random_cocktail/', views.create_random_cocktail, name='create_random_cocktail'),
    path('list_possible_cocktails/', views.list_possible_cocktails, name='list_possible_cocktails'),
    path('list_almost_possible_cocktails/', views.list_almost_possible_cocktails, name='list_almost_possible_cocktails'),
    path('list_cocktails_with_alternatives/', views.list_cocktails_with_alternatives, name='list_cocktails_with_alternatives'),
]

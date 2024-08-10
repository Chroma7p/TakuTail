from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cocktails', views.CocktailViewSet)

urlpatterns = [
    path('', views.cocktail_list, name='cocktails_list'),
    path('create_random_cocktail/', views.create_random_cocktail, name='create_random_cocktail'),
    path('<int:pk>/', views.cocktail_detail, name='cocktail_detail'),
    path('list_possible_cocktails/', views.list_cocktails, name='list_possible_cocktails'),
]

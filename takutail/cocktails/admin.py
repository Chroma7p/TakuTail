from django.contrib import admin
from .models import Cocktail, CocktailIngredient, CocktailName

@admin.register(Cocktail)
class CocktailAdmin(admin.ModelAdmin):
    list_display = ('name', 'generated_name')

@admin.register(CocktailIngredient)
class CocktailIngredientAdmin(admin.ModelAdmin):
    list_display = ('cocktail', 'ingredient_id', 'ingredient_type', 'amount')

@admin.register(CocktailName)
class CocktailNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'base', 'ingredient1', 'ingredient2', 'ingredient3', 'ingredient4', 'top', 'middle', 'bottom')

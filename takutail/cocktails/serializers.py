from rest_framework import serializers
from .models import Cocktail, CocktailIngredient, CocktailName

class CocktailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cocktail
        fields = '__all__'

class CocktailIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailIngredient
        fields = '__all__'

class CocktailNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CocktailName
        fields = '__all__'

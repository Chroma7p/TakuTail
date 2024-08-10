from django.db import models
from core.models import Sake, Wari, Other

class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    generated_name = models.CharField(max_length=100, blank=True, null=True)
    base = models.CharField(max_length=100, null=True)
    base_amount = models.CharField(max_length=100, null=True)
    ingredient1 = models.CharField(max_length=100, blank=True, null=True)
    amount1 = models.CharField(max_length=100, blank=True, null=True)
    ingredient2 = models.CharField(max_length=100, blank=True, null=True)
    amount2 = models.CharField(max_length=100, blank=True, null=True)
    ingredient3 = models.CharField(max_length=100, blank=True, null=True)
    amount3 = models.CharField(max_length=100, blank=True, null=True)
    ingredient4 = models.CharField(max_length=100, blank=True, null=True)
    amount4 = models.CharField(max_length=100, blank=True, null=True)
    ingredient5 = models.CharField(max_length=100, blank=True, null=True)
    amount5 = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class CocktailIngredient(models.Model):
    COCKTAIL_TYPE_CHOICES = [
        ('SAKE', 'Sake'),
        ('WARI', 'Wari'),
        ('OTHER', 'Other')
    ]
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    ingredient_id = models.PositiveIntegerField()
    ingredient_type = models.CharField(max_length=10, choices=COCKTAIL_TYPE_CHOICES)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.cocktail.name} - {self.ingredient_type} - {self.amount}"

class CocktailName(models.Model):
    name = models.CharField(max_length=100)
    base = models.CharField(max_length=100)
    ingredient1 = models.CharField(max_length=100)
    ingredient2 = models.CharField(max_length=100, blank=True, null=True)
    ingredient3 = models.CharField(max_length=100, blank=True, null=True)
    ingredient4 = models.CharField(max_length=100, blank=True, null=True)
    top = models.BooleanField(default=False)
    middle = models.BooleanField(default=False)
    bottom = models.BooleanField(default=False)

    def __str__(self):
        return self.name

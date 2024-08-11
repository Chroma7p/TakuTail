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
    recipe = models.TextField(blank=True, null=True)
    alcohol_content = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def calculate_alcohol_content(self):
        ingredients = [
            (self.base, self.base_amount),
            (self.ingredient1, self.amount1),
            (self.ingredient2, self.amount2),
            (self.ingredient3, self.amount3),
            (self.ingredient4, self.amount4),
            (self.ingredient5, self.amount5),
        ]

        total_volume = 0
        total_alcohol = 0

        for ingredient_name, amount in ingredients:
            if ingredient_name and amount:
                try:
                    volume = float(amount.replace('ml', ''))
                except ValueError:
                    volume = 0
                total_volume += volume

                alcohol_percentage = 0

                # Sake, Wari, Other モデルから該当するインスタンスを取得
                try:
                    ingredient = Sake.objects.filter(name=ingredient_name).first()
                    if ingredient:
                        alcohol_percentage = ingredient.alcohol_content
                        if type(alcohol_percentage) == str:
                            try:
                                alcohol_percentage = float(alcohol_percentage.replace('%', ''))
                            except ValueError:
                                alcohol_percentage = 0
                                
                except Sake.DoesNotExist:
                    pass

                if not ingredient:
                    try:
                        ingredient = Wari.objects.filter(name=ingredient_name).first()
                        if ingredient:
                            alcohol_percentage = 0  # Wariのアルコール度数がない場合は0
                    except Wari.DoesNotExist:
                        pass

                if not ingredient:
                    try:
                        ingredient = Other.objects.filter(name=ingredient_name).first()
                        if ingredient:
                            alcohol_percentage = 0  # Otherのアルコール度数がない場合は0
                    except Other.DoesNotExist:
                        pass

                total_alcohol += volume * (alcohol_percentage / 100)

        if total_volume == 0:
            return 0
        return (total_alcohol / total_volume) * 100

    def save(self, *args, **kwargs):
        self.alcohol_content = self.calculate_alcohol_content()
        super().save(*args, **kwargs)
    
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

# cocktails/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cocktail, CocktailName, CocktailIngredient
from core.models import Sake, Wari, Other
from .serializers import CocktailSerializer
import random


class Ingredient:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer

class CocktailObject:
    def __init__(self, name, ingredients):
        self.name = str(name).strip()
        self.ingredients = ingredients

        # Check if all ingredients are available
        for ingredient in ingredients:
            if ingredient.item is None:
                raise ValueError(f"Missing ingredient for cocktail {name}")

    def display_ingredients_tree(self):
        tree = f'カクテル: {self.name}\n'
        for ingredient in self.ingredients:
            tree += f'  ├─ 材料: {ingredient.item.name} - {ingredient.amount}\n'
        return tree

    def generate_name(self, cocktail_name_list):
        other_names = [ing.item.name for ing in self.ingredients if isinstance(ing.item, Other)]
        base_names = [ing.item.name for ing in self.ingredients if isinstance(ing.item, Sake)]
        wari_names = [ing.item.name for ing in self.ingredients if isinstance(ing.item, Wari)]

        # Combine all ingredient names
        combined_names = other_names + base_names + wari_names
        
        print(combined_names   )
        add_top = []
        add_middle = []
        add_bottom = []
        end = False
        # Check for matching rules in cocktail_name_list
        for rules in cocktail_name_list:
            cocktail_name = rules.name
            print(rules.name, rules.ingredient1, rules.ingredient2, rules.ingredient3, rules.ingredient4, rules.base)
            if all(ingredient in combined_names for ingredient in [rules.base, rules.ingredient1, rules.ingredient2, rules.ingredient3, rules.ingredient4] if ingredient):
                combined_names = [name for name in combined_names if name not in  [rules.base, rules.ingredient1, rules.ingredient2, rules.ingredient3, rules.ingredient4] ]

                while True:
                    c = random.choice(["top", "middle", "bottom"])
                    if c == "top" and rules.top:
                        add_top.append(cocktail_name)
                        break
                    if c == "bottom" and rules.bottom:
                        add_bottom.append(cocktail_name)
                        break
                    if c == "middle" and rules.middle:
                        add_middle.append(cocktail_name)
                        break
        random.shuffle(add_top)
        random.shuffle(add_bottom)
        random.shuffle(add_middle)
        combined_names = add_top + combined_names + add_bottom
        for s in add_middle:
            if len(combined_names) == 0:
                combined_names.append(s)
            elif len(combined_names) == 1:
                combined_names.insert(random.randint(0, 1), s)
            else:
                combined_names.insert(random.randint(1, len(combined_names) - 1), s)
                
        print(combined_names)

        # Generate the final name
        final_name = ' '.join(combined_names)
        return final_name

@api_view(['GET'])
def create_random_cocktail(request):
    # ベースの酒を1か2ランダムに選択
    base_count = random.randint(1, 2)
    sakes = random.sample(list(Sake.objects.all()), base_count)

    # 割り材を1から3ランダムに選択
    wari_count = random.randint(1, 3)
    waris = random.sample(list(Wari.objects.all()), wari_count)

    # その他の材料を0から1つ選択
    other_count = random.randint(0, 1)
    others = random.sample(list(Other.objects.all()), other_count)
    
    # 選択された材料をまとめる
    ingredients = [Ingredient(sake, '適量') for sake in sakes] + \
                  [Ingredient(wari, '適量') for wari in waris] + \
                  [Ingredient(other, '適量') for other in others]

    # ランダムカクテルの作成
    random_cocktail_object = CocktailObject("ランダムカクテル", ingredients)
    random_cocktail_name = random_cocktail_object.generate_name(CocktailName.objects.all())

    # データベースに保存
    random_cocktail = Cocktail(
        name=random_cocktail_object.name,
        generated_name=random_cocktail_name,
        base=ingredients[0].item.name if len(ingredients) > 0 else None,
        base_amount=ingredients[0].amount if len(ingredients) > 0 else None,
        ingredient1=ingredients[1].item.name if len(ingredients) > 1 else None,
        amount1=ingredients[1].amount if len(ingredients) > 1 else None,
        ingredient2=ingredients[2].item.name if len(ingredients) > 2 else None,
        amount2=ingredients[2].amount if len(ingredients) > 2 else None,
        ingredient3=ingredients[3].item.name if len(ingredients) > 3 else None,
        amount3=ingredients[3].amount if len(ingredients) > 3 else None,
        ingredient4=ingredients[4].item.name if len(ingredients) > 4 else None,
        amount4=ingredients[4].amount if len(ingredients) > 4 else None,
        ingredient5=ingredients[5].item.name if len(ingredients) > 5 else None,
        amount5=ingredients[5].amount if len(ingredients) > 5 else None
    )
    random_cocktail.save()


    # 結果の表示
    serializer = CocktailSerializer(random_cocktail)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


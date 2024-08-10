# cocktails/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cocktail, CocktailName, CocktailIngredient
from core.models import Sake, Wari, Other
from .serializers import CocktailSerializer
from users.models import UserSake, UserWari, UserOther
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import random


class Ingredient:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount

class CocktailViewSet(viewsets.ModelViewSet):
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer
    
    
class PossibleCocktailViewSet(viewsets.ViewSet):
    template_name = 'cocktails/possible_cocktails.html'
    queryset = Cocktail.objects.all()
    serializer_class = CocktailSerializer


def cocktail_detail(request, pk):
    cocktail = get_object_or_404(Cocktail, pk=pk)
    return render(request, 'cocktails/cocktail_detail.html', {'cocktail': cocktail})
def cocktail_list(request):
    cocktails = Cocktail.objects.all()
    return render(request, 'cocktails/cocktail_list.html', {'cocktails': cocktails})


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


        # Generate the final name
        final_name = ' '.join(combined_names)
        return final_name


def create_random_cocktail(request):
    base_count = random.randint(1, 2)
    sakes = random.sample(list(Sake.objects.all()), base_count)

    wari_count = random.randint(1, 3)
    waris = random.sample(list(Wari.objects.filter(exclude=False)), wari_count)
    print(list(Wari.objects.filter(exclude=False)))
    other_count = random.randint(0, 1)
    others = random.sample(list(Other.objects.filter(exclude=False)), other_count)
    print(list(Other.objects.filter(exclude=False)))
    
    # 選択された材料をまとめる
    ingredients = [Ingredient(sake, '適量') for sake in sakes] + \
                  [Ingredient(wari, '適量') for wari in waris] + \
                  [Ingredient(other, '適量') for other in others]

    # ランダムカクテルの作成
    random_cocktail_object = CocktailObject("ランダムカクテル", ingredients)
    random_cocktail_name = random_cocktail_object.generate_name(CocktailName.objects.all())

    return render(request, 'cocktails/random_cocktail.html', {
        'cocktail_name': random_cocktail_name,
        'ingredients': ingredients,
    })




ALTERNATIVE_INGREDIENTS = {
    'レモンジュース': ['ライムジュース'],
    'ライムジュース': ['レモンジュース'],
    'ジン': ['ウォッカ', '焼酎'],
    'ウォッカ': ['ジン', '焼酎'],
    '焼酎': ['ジン', 'ウォッカ'],
    '白ワイン': ['スパークリングワイン'],
    'スパークリングワイン': ['白ワイン'],
    'トニックウォーター': ['ジンジャーエール', 'グレープフルーツジュース'],
    'ジンジャーエール': ['トニックウォーター', 'グレープフルーツジュース'],
    'グレープフルーツジュース': ['トニックウォーター', 'ジンジャーエール'],
    'ホワイトラム': ['ダークラム', 'テキーラ'],
    'ダークラム': ['ホワイトラム', 'テキーラ'],
    'テキーラ': ['ホワイトラム', 'ダークラム'],
    'みりん': ['日本酒'],
    '日本酒': ['みりん'],
    '生クリーム': ['牛乳'],
    '牛乳': ['生クリーム'],
    '炭酸水': ['サイダー'],
    'サイダー': ['炭酸水'],
}

def get_user_ingredients(user):
    user_sakes = UserSake.objects.filter(user=user)
    user_waris = UserWari.objects.filter(user=user)
    user_others = UserOther.objects.filter(user=user)

    user_sake_names = [user_sake.sake.name for user_sake in user_sakes if user_sake.owned]
    user_wari_names = [user_wari.wari.name for user_wari in user_waris if user_wari.owned]
    user_other_names = [user_other.other.name for user_other in user_others if user_other.owned]

    return set(user_sake_names + user_wari_names + user_other_names)

def get_possible_cocktails(user_ingredients):
    possible_cocktails = []
    for cocktail in Cocktail.objects.all():
        ingredients = [
            cocktail.base,
            cocktail.ingredient1,
            cocktail.ingredient2,
            cocktail.ingredient3,
            cocktail.ingredient4,
            cocktail.ingredient5,
        ]
        ingredients = [ingredient for ingredient in ingredients if ingredient]  # 空の材料を取り除く

        if all(ingredient in user_ingredients for ingredient in ingredients):
            possible_cocktails.append(cocktail)
    return possible_cocktails

def get_almost_possible_cocktails(user_ingredients):
    almost_possible_cocktails = []
    for cocktail in Cocktail.objects.all():
        ingredients = [
            cocktail.base,
            cocktail.ingredient1,
            cocktail.ingredient2,
            cocktail.ingredient3,
            cocktail.ingredient4,
            cocktail.ingredient5,
        ]
        ingredients = [ingredient for ingredient in ingredients if ingredient]  # 空の材料を取り除く

        missing_ingredients = [ingredient for ingredient in ingredients if ingredient not in user_ingredients]

        if len(missing_ingredients) == 1:
            almost_possible_cocktails.append({
                'cocktail': cocktail,
                'missing_ingredient': missing_ingredients[0]
            })
    return almost_possible_cocktails

def get_possible_cocktails_with_alternatives(user_ingredients):
    possible_cocktails_with_alternatives = []
    for cocktail in Cocktail.objects.all():
        ingredients = [
            cocktail.base,
            cocktail.ingredient1,
            cocktail.ingredient2,
            cocktail.ingredient3,
            cocktail.ingredient4,
            cocktail.ingredient5,
        ]
        ingredients = [ingredient for ingredient in ingredients if ingredient]  # 空の材料を取り除く

        missing_ingredients = [ingredient for ingredient in ingredients if ingredient not in user_ingredients]
        alternative_used = {}
        alternatives_needed = False

        if len(missing_ingredients) > 0:
            for missing in missing_ingredients:
                if missing in ALTERNATIVE_INGREDIENTS:
                    for alternative in ALTERNATIVE_INGREDIENTS[missing]:
                        if alternative in user_ingredients:
                            alternative_used[missing] = alternative
                            alternatives_needed = True
                            break

        # alternatives_needed が True の場合のみリストに追加
        if alternatives_needed:
            final_ingredients = set(ingredients) - set(missing_ingredients) | set(alternative_used.values())
            if len(ingredients) == len(final_ingredients):
                possible_cocktails_with_alternatives.append({
                    'cocktail': cocktail,
                    'missing_ingredients': list(alternative_used.items())
                })
    return possible_cocktails_with_alternatives

@login_required
def list_cocktails(request):
    user = request.user
    user_ingredients = get_user_ingredients(user)

    possible_cocktails = get_possible_cocktails(user_ingredients)
    almost_possible_cocktails = get_almost_possible_cocktails(user_ingredients)
    possible_cocktails_with_alternatives = get_possible_cocktails_with_alternatives(user_ingredients)

    almost_possible_cocktails_result = [
        {
            'cocktail': CocktailSerializer(cocktail['cocktail']).data,
            'missing_ingredient': cocktail['missing_ingredient']
        }
        for cocktail in almost_possible_cocktails
    ]

    cocktails_with_alternatives_result = [
        {
            'cocktail': CocktailSerializer(cocktail['cocktail']).data,
            'missing_ingredients': cocktail['missing_ingredients']
        }
        for cocktail in possible_cocktails_with_alternatives
    ]

    return render(request, 'cocktails/possible_cocktails.html', {
        'possible_cocktails': CocktailSerializer(possible_cocktails, many=True).data,
        'almost_possible_cocktails': almost_possible_cocktails_result,
        'cocktails_with_alternatives': cocktails_with_alternatives_result,
    })
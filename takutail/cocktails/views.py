# cocktails/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Cocktail, CocktailName, CocktailIngredient
from core.models import Sake, Wari, Other
from .serializers import CocktailSerializer
from users.models import UserSake, UserWari, UserOther
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

@api_view(['GET'])
def list_possible_cocktails(request):
    user = request.user

    user_sakes = UserSake.objects.filter(user=user)
    user_waris = UserWari.objects.filter(user=user)
    user_others = UserOther.objects.filter(user=user)

    user_sake_names = [user_sake.sake.name for user_sake in user_sakes]
    user_wari_names = [user_wari.wari.name for user_wari in user_waris]
    user_other_names = [user_other.other.name for user_other in user_others]

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

        if all(ingredient in user_sake_names + user_wari_names + user_other_names for ingredient in ingredients if ingredient):
            possible_cocktails.append(cocktail)

    serializer = CocktailSerializer(possible_cocktails, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_almost_possible_cocktails(request):
    user = request.user

    user_sakes = UserSake.objects.filter(user=user)
    user_waris = UserWari.objects.filter(user=user)
    user_others = UserOther.objects.filter(user=user)

    user_sake_names = [user_sake.sake.name for user_sake in user_sakes]
    user_wari_names = [user_wari.wari.name for user_wari in user_waris]
    user_other_names = [user_other.other.name for user_other in user_others]

    user_ingredients = set(user_sake_names + user_wari_names + user_other_names)

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

    result = [
        {
            'cocktail': CocktailSerializer(cocktail['cocktail']).data,
            'missing_ingredient': cocktail['missing_ingredient']
        }
        for cocktail in almost_possible_cocktails
    ]

    return Response(result)


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

def get_possible_ingredients(user_ingredients):
    possible_ingredients = set(user_ingredients)
    for ingredient in user_ingredients:
        if ingredient in ALTERNATIVE_INGREDIENTS:
            possible_ingredients.update(ALTERNATIVE_INGREDIENTS[ingredient])
    return possible_ingredients

@api_view(['GET'])
def list_cocktails_with_alternatives(request):
    user = request.user

    user_sakes = UserSake.objects.filter(user=user)
    user_waris = UserWari.objects.filter(user=user)
    user_others = UserOther.objects.filter(user=user)

    user_sake_names = [user_sake.sake.name for user_sake in user_sakes]
    user_wari_names = [user_wari.wari.name for user_wari in user_waris]
    user_other_names = [user_other.other.name for user_other in user_others]

    user_ingredients = set(user_sake_names + user_wari_names + user_other_names)
    possible_ingredients = get_possible_ingredients(user_ingredients)

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

        missing_ingredients = [ingredient for ingredient in ingredients if ingredient not in user_ingredients]
        alternative_used = {}

        # そのまま作れるカクテルは除外
        if len(missing_ingredients) == 0:
            continue

        if len(missing_ingredients) > 0:
            for missing in missing_ingredients:
                if missing in ALTERNATIVE_INGREDIENTS:
                    for alternative in ALTERNATIVE_INGREDIENTS[missing]:
                        if alternative in user_ingredients:
                            alternative_used[missing] = alternative
                            break

        final_ingredients = set(ingredients) - set(missing_ingredients) | set(alternative_used.values())

        if len(ingredients) == len(final_ingredients):
            possible_cocktails.append({
                'cocktail': cocktail,
                'missing_ingredients': list(alternative_used.items())
            })

    result = [
        {
            'cocktail': CocktailSerializer(cocktail['cocktail']).data,
            'missing_ingredients': cocktail['missing_ingredients']
        }
        for cocktail in possible_cocktails
    ]

    return Response(result)
from rest_framework import viewsets
from .models import UserSake, UserWari, UserOther
from .serializers import UserSakeSerializer, UserWariSerializer, UserOtherSerializer

from django.contrib.auth.decorators import login_required
from core.models import Sake, Wari, Other
from django.http import JsonResponse
from django.shortcuts import render


@login_required
def toggle_ownership(request, item_type, item_id):
    user = request.user

    if item_type == 'sake':
        item = UserSake.objects.get(user=user, sake_id=item_id)
    elif item_type == 'wari':
        item = UserWari.objects.get(user=user, wari_id=item_id)
    elif item_type == 'other':
        item = UserOther.objects.get(user=user, other_id=item_id)
    else:
        return JsonResponse({'error': 'Invalid item type'}, status=400)

    item.owned = not item.owned
    item.save()

    return JsonResponse({'status': 'success', 'new_owned': item.owned})

@login_required
def ingredients_list(request):
    user = request.user

    # ユーザーの材料データが初期化されていない場合に初期化
    if not UserSake.objects.filter(user=user).exists():
        sakes = Sake.objects.all()
        for sake in sakes:
            UserSake.objects.create(user=user, sake=sake, owned=False)
    
    if not UserWari.objects.filter(user=user).exists():
        waris = Wari.objects.all()
        for wari in waris:
            UserWari.objects.create(user=user, wari=wari, owned=False)
    
    if not UserOther.objects.filter(user=user).exists():
        others = Other.objects.all()
        for other in others:
            UserOther.objects.create(user=user, other=other, owned=False)

    # ユーザーの材料データを取得
    user_sakes = UserSake.objects.filter(user=user)
    user_waris = UserWari.objects.filter(user=user)
    user_others = UserOther.objects.filter(user=user)

    return render(request, 'users/ingredients_list.html', {
        'user_sakes': user_sakes,
        'user_waris': user_waris,
        'user_others': user_others,
    })
class UserSakeViewSet(viewsets.ModelViewSet):
    queryset = UserSake.objects.all()
    serializer_class = UserSakeSerializer

class UserWariViewSet(viewsets.ModelViewSet):
    queryset = UserWari.objects.all()
    serializer_class = UserWariSerializer

class UserOtherViewSet(viewsets.ModelViewSet):
    queryset = UserOther.objects.all()
    serializer_class = UserOtherSerializer

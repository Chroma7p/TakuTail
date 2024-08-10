from rest_framework import viewsets
from .models import UserSake, UserWari, UserOther
from .serializers import UserSakeSerializer, UserWariSerializer, UserOtherSerializer

class UserSakeViewSet(viewsets.ModelViewSet):
    queryset = UserSake.objects.all()
    serializer_class = UserSakeSerializer

class UserWariViewSet(viewsets.ModelViewSet):
    queryset = UserWari.objects.all()
    serializer_class = UserWariSerializer

class UserOtherViewSet(viewsets.ModelViewSet):
    queryset = UserOther.objects.all()
    serializer_class = UserOtherSerializer

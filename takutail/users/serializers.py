from rest_framework import serializers
from .models import UserSake, UserWari, UserOther

class UserSakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSake
        fields = '__all__'

class UserWariSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWari
        fields = '__all__'

class UserOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOther
        fields = '__all__'

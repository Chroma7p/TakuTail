from rest_framework import serializers
from .models import Sake, Wari, Other

class SakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sake
        fields = '__all__'

class WariSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wari
        fields = '__all__'

class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = '__all__'

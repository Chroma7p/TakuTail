from rest_framework import viewsets
from core.models import Sake, Wari, Other
from .serializers import SakeSerializer, WariSerializer, OtherSerializer

class SakeViewSet(viewsets.ModelViewSet):
    queryset = Sake.objects.all()
    serializer_class = SakeSerializer

class WariViewSet(viewsets.ModelViewSet):
    queryset = Wari.objects.all()
    serializer_class = WariSerializer

class OtherViewSet(viewsets.ModelViewSet):
    queryset = Other.objects.all()
    serializer_class = OtherSerializer

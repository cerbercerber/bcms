from rest_framework import viewsets
from bo.models import *
from .serializers import *


class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all()
    serializer_class = EleveSerializer
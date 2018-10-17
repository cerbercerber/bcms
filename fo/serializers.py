from rest_framework import serializers
from bo.models import *
class EleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleve
        fields = '__all__'
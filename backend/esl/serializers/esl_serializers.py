from rest_framework import serializers

from backend.esl.models.esl import *

from esl.serializers.rack_serializers import RackSerializer

class ESLSerializer(serializers.ModelSerializer):
    rack=RackSerializer()

    class Meta:
        model=ESL
        fields="__all__"
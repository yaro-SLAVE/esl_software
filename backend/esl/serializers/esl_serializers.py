from rest_framework import serializers

from esl.models import *

from esl.serializers.rack_serializers import RackSerializer

class ESLSerializer(serializers.ModelSerializer):
    rack=RackSerializer()

    class Meta:
        model=ESL
        fields="__all__"
from rest_framework import serializers

from esl.models.esl import *

from esl.serializers.rack_serializers import RackSerializer

class ESLSerializer(serializers.ModelSerializer):
    class Meta:
        model=ESL
        fields=['id', 'esl_ip', 'rack']

class ESLCreateSerializer(serializers.Serializer):
    ip = serializers.CharField()
    rack = serializers.IntegerField()
    token = serializers.CharField()
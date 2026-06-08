from rest_framework import serializers

from esl.models.esl import *

from esl.serializers.rack_serializers import RackSerializer

class ESLSerializer(serializers.ModelSerializer):
    rack = RackSerializer()
    class Meta:
        model=ESL
        fields=['id', 'esl_ip', 'rack']

class ESLCreateSerializer(serializers.Serializer):
    ip = serializers.CharField(required = False)
    rack = serializers.IntegerField()
    token = serializers.CharField()

class ESLErrorSerializer(serializers.Serializer):
    rack = serializers.CharField()
    channel = serializers.CharField()
    status = serializers.CharField()

class ESLErrorListSerializer(serializers.ModelSerializer):
    esl = ESLSerializer()
    class Meta:
        model = ESLError
        fields = ['id', 'status', 'date', 'channel', 'esl']
    

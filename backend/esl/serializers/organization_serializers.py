from rest_framework import serializers

from esl.models import *

from esl.serializers.auth_serializers import UserSerializer

class OrganizationSerializer(serializers.ModelSerializer):
    general_manager=UserSerializer()

    class Meta:
        model=Organization
        fields="__all__"

class OrganizationFilialSerializer(serializers.ModelSerializer):
    organization=OrganizationSerializer()

    class Meta:
        model=OrganizationFilial
        fields="__all__"

class IntegrationSerializer(serializers.ModelSerializer):
    organization=OrganizationSerializer

    class Meta:
        model=Integration
        fields="__all__"
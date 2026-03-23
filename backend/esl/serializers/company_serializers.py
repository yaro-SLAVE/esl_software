from rest_framework import serializers

from esl.models.company import *
from esl.models.profile import *

from esl.serializers.auth_serializers import UserProfileSerializer

class CompanySerializer(serializers.ModelSerializer):
    administrators=serializers.SerializerMethodField()

    class Meta:
        model=Company
        fields=["id", "name"]

    def get_administrators(self, obj: Company):
        profiles = UserProfile.objects.filter(role="admin", company=obj).all()
        return UserProfileSerializer(profiles, many=True).data

class CompanyFilialSerializer(serializers.ModelSerializer):

    class Meta:
        model=CompanyFilial
        fields=["id", "name"]

class IntegrationCretaeSerializer(serializers.Serializer):
    login=serializers.CharField()
    password=serializers.CharField()
    url=serializers.CharField()
    type=serializers.CharField()

class IntegrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Company
        fields=['id', 'integration_type', 'integration_url']
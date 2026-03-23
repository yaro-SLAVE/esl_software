from rest_framework import serializers

from django.contrib.auth.models import User

from esl.models.profile import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=["username", "first_name", "last_name", "is_superuser"]

class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    is_auth=serializers.SerializerMethodField()

    class Meta:
        model=UserProfile
        fields=["role", "user", "filial_id", "company_id", "is_auth"]
    
    def get_is_auth(self, obj):
        return obj is not None
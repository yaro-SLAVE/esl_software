from rest_framework import serializers

from django.contrib.auth.models import User

from esl.models import *

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields="__all__"

class UserProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()

    class Meta:
        model=UserProfile
        fields="__all__"
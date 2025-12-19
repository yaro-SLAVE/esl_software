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

class ShelfSerializer(serializers.ModelSerializer):
    filial=OrganizationFilialSerializer()

    class Meta:
        model=Shelf
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    shelf=ShelfSerializer

    class Meta:
        model=Product
        fields="__all__"

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Item
        fields="__all__"
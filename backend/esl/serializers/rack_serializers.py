from rest_framework import serializers

from esl.models import *

from esl.serializers.organization_serializers import OrganizationFilialSerializer

class RackSerializer(serializers.ModelSerializer):
    filial=OrganizationFilialSerializer()

    class Meta:
        model=Rack
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    rack=RackSerializer()

    class Meta:
        model=Product
        fields="__all__"

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Item
        fields="__all__"
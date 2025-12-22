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
        fields=['id', 'short_name', 'barcode']

class ProductShowSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=['short_name', 'description', 'price', 'prev_price', 'have_promotion', 'barcode']
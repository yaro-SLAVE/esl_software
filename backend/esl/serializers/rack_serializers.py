from rest_framework import serializers

from esl.models import *

from esl.serializers.organization_serializers import OrganizationFilialSerializer

class RackSerializer(serializers.ModelSerializer):
    filial=OrganizationFilialSerializer()

    class Meta:
        model=Rack
        fields="__all__"

class ProductToRackUpdateSerializer(serializers.Serializer):
    shelf = serializers.IntegerField()
    number = serializers.IntegerField()
    id = serializers.IntegerField()

class RackUpdateSerializer(serializers.Serializer):
    products = ProductToRackUpdateSerializer(many=True)

    def update(self, instance, validated_data):
        products_to_delete = Product.objects.filter(rack = instance).all()

        for product in products_to_delete:
            product.rack = None
            product.shelf = 0
            product.number = 0
            product.save()
        
        products_to_add = validated_data["products"]

        for product in products_to_add:
            product_to_change = Product.objects.filter(pk = product["id"]).first()
            product_to_change.rack = instance
            product_to_change.shelf = product["shelf"]
            product_to_change.number = product["number"]
            product_to_change.save()

        return validated_data

class ProductSerializer(serializers.ModelSerializer):
    rack=RackSerializer()

    class Meta:
        model=Product
        fields=['id', 'short_name', 'barcode']

class ProductShowSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=['short_name', 'description', 'price', 'prev_price', 'have_promotion', 'barcode']
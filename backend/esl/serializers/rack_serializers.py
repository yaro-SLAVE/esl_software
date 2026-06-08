from dataclasses import asdict

from rest_framework import serializers

from esl.models.company import *
from esl.models.rack import *

from esl.serializers.company_serializers import CompanySerializer, CompanyFilialSerializer

from esl.onec_1c.services import get_product_info

class RackListSerializer(serializers.Serializer):
    class FilialSerializer(serializers.Serializer):
        name=serializers.CharField()
        rows=serializers.IntegerField()
        columns=serializers.IntegerField()

    class RackSerilizer(serializers.Serializer):
        class ProductSerializer(serializers.Serializer):
            id=serializers.IntegerField()
            external_id=serializers.CharField()
            short_name=serializers.CharField()
            shelf=serializers.IntegerField()
            number=serializers.IntegerField()

        id=serializers.IntegerField()
        row=serializers.IntegerField()
        column=serializers.IntegerField()
        number=serializers.CharField()
        esl_ip=serializers.CharField()
        products=ProductSerializer(many=True)

    filial=FilialSerializer()
    racks=RackSerilizer(many=True)

class ProductToRackUpdateSerializer(serializers.Serializer):
    shelf = serializers.IntegerField()
    number = serializers.IntegerField()
    external_id = serializers.CharField(required=False)
    id = serializers.IntegerField(required=False)
    short_name = serializers.CharField(required=False)

class RackUpdateSerializer(serializers.Serializer):
    products = ProductToRackUpdateSerializer(many=True, required=False)
    row = serializers.IntegerField(required=False)
    column = serializers.IntegerField(required=False)
    order_change = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        if "products" in validated_data:
            if 'order_change' in validated_data:
                products_to_change = validated_data["products"]

                for product in products_to_change:
                    product_to_add = Product.objects.filter(pk = product["id"]).first()
                    product_to_add.number = product["number"]
                    product_to_add.save()
            
            else:
                products_to_add = validated_data["products"]

                products_in_rack = Product.objects.filter(rack = instance).all()

                for product in products_to_add:
                    if product['number'] < len(products_in_rack):
                        product_to_delete = Product.objects.filter(rack = instance, number = product['number'], shelf = product['shelf']).first()

                        if (product_to_delete is not None):
                            product_to_delete.delete()
                    
                    product_to_add= Product.objects.create(
                        external_id=product["external_id"],
                        shelf = product["shelf"],
                        number = product["number"],
                        rack=instance,
                        short_name = product["short_name"]
                    )
        
        elif "row" in validated_data:
            instance.row =validated_data["row"]
            instance.column =validated_data["column"]
            instance.save()

        return validated_data

class RackSerializer(serializers.ModelSerializer):
    filial=CompanyFilialSerializer

    class Meta:
        model=Rack
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id', 'short_name', 'external_id', 'rack']

class ProductFilialListSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    short_name = serializers.CharField()

class ProductShowSerializer(serializers.Serializer):
    id = serializers.CharField()
    short_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    have_promotion = serializers.BooleanField()
    promotion = serializers.IntegerField()

class ProductsExternalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "short_name"]

class UpdateProductSerializer(serializers.Serializer):
    class UpdateProductItemSerializer(serializers.Serializer):
        id = serializers.CharField()
        short_name = serializers.CharField(required=False, allow_null=True, default=None)
        have_promotion = serializers.BooleanField(required=False, allow_null=True, default=None)
        promotion = serializers.IntegerField(required=False, allow_null=True, default=None)
        price = serializers.FloatField(required=False, allow_null=True, default=None)

    updates = UpdateProductItemSerializer(many=True)
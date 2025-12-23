from rest_framework import serializers

from esl.models import *

from esl.serializers.organization_serializers import OrganizationFilialSerializer

class RackListSerializer(serializers.Serializer):
    class FilialSerializer(serializers.Serializer):
        organization_name=serializers.CharField()
        address=serializers.CharField()
        rows=serializers.IntegerField()
        columns=serializers.IntegerField()

    class RackSerilizer(serializers.Serializer):
        class ProductSerializer(serializers.Serializer):
            barcode=serializers.CharField()
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
    id = serializers.IntegerField()

class RackUpdateSerializer(serializers.Serializer):
    products = ProductToRackUpdateSerializer(many=True)
    row = serializers.IntegerField(required=False)
    column = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        print(validated_data["products"])
        if "products" in validated_data:
            products_to_delete = Product.objects.filter(rack = instance).all()

            for product in products_to_delete:
                product.rack = None
                product.shelf = -1
                product.number = -1
                product.save()
            
            products_to_add = validated_data["products"]

            for product in products_to_add:
                product_to_change = Product.objects.filter(pk = product["id"]).first()
                product_to_change.rack = instance
                product_to_change.shelf = product["shelf"]
                product_to_change.number = product["number"]
                product_to_change.save()
        
        elif "row" in validated_data:
            instance.row =validated_data["row"]
            instance.column =validated_data["column"]
            instance.save()

        return validated_data

class RackSerializer(serializers.ModelSerializer):
    filial=OrganizationFilialSerializer

    class Meta:
        model=Rack
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    rack=RackSerializer()

    class Meta:
        model=Product
        fields=['id', 'short_name', 'barcode', 'rack']

class ProductShowSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        fields=['short_name', 'description', 'price', 'prev_price', 'have_promotion', 'barcode']
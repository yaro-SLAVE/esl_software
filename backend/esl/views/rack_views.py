from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models import *

from esl.serializers.rack_serializers import *

from aiohttp import ClientSession, ClientResponseError
from django.http import Http404

from rest_framework import serializers

from rest_framework.response import Response

from esl.esl.api.product import send_product, ESLResponse


class RackViewset(
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet
):
    class ESLSerializer(serializers.Serializer):
        name = serializers.CharField()
        price = serializers.FloatField()
        barcode = serializers.CharField()

    queryset=Rack.objects.all()
    serializer_class=RackSerializer
    permission_classes=[IsAuthenticated]

    def update(self, request, *args, **kwargs):
        rack = super().update(request, *args, **kwargs)

        product = Product.objects.filter(rack = rack).first()

        serializer = self.Serializer(data={
            'name': product.short_name,
            'price': product.price,
            'barcode': product.barcode
        })
        serializer.is_valid(raise_exception=True)

        token = 'qwe123123qwe'

        with ClientSession() as client:
            response: ESLResponse | None = None

            response = send_product(
                client, 
                serializer.validated_data["name"], 
                serializer.validated_data["price"], 
                serializer.validated_data["barcode"],
                token
            )
        
        return rack



class ProductViewset(
    ListModelMixin,
    GenericViewSet
):
    queryset=Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'show_product':
            return ProductShowSerializer
        else:
            return ProductSerializer

    @action(['GET'], url_path=r"show/(?P<barcode>[a-z0-9]+)", detail=False)
    def show_product(self, request, barcode): 
        product = self.get_queryset().get(barcode=barcode)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
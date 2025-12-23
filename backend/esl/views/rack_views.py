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

import asyncio


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

    def get_serializer_class(self):
        if self.action == "update":
            return RackUpdateSerializer
        elif self.action == "list":
            return RackListSerializer
        else: 
            return RackSerializer
        
    def list(self, request, *args, **kwargs):
        filial_id = request.GET.get('filial') 
        filial = OrganizationFilial.objects.filter(pk=filial_id).first()

        racks = self.get_queryset().filter(filial=filial)

        response = {
            "filial": {
                "organization_name": filial.organization.name,
                "address": filial.address,
                "rows": filial.rows,
                "columns": filial.columns
            },
            "racks": []
        }

        for rack in racks:
            esl = ESL.objects.get(rack=rack)
            products = Product.objects.filter(rack=rack).all()

            response["racks"].append({
                "id": rack.id,
                "row": rack.row,
                "column": rack.column,
                "number": rack.number,
                "esl_ip": esl.esl_ip,
                "products": [
                    {
                        "barcode": product.barcode,
                        "short_name": product.short_name,
                        "shelf": product.shelf,
                        "number": product.number
                    } for product in products
                ]
            })

        print(response)
        
        serializer = self.get_serializer(response)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        r = super().update(request, *args, **kwargs)

        pk = self.kwargs["pk"]

        rack = Rack.objects.filter(pk=pk).first()

        product = Product.objects.filter(rack = rack).first()

        serializer = self.ESLSerializer(data={
            'name': product.short_name,
            'price': product.price,
            'barcode': product.barcode
        })
        serializer.is_valid(raise_exception=True)

        esl = ESL.objects.filter(rack = rack).first()

        asyncio.run(self.send_to_esl(
                    serializer.validated_data,
                    esl.token,
                    esl.esl_ip
                ))
                
        return r

    async def send_to_esl(self, data, token, esl_ip):
        async with ClientSession() as client:
            try:
                response = await send_product(
                    client, 
                    data["name"], 
                    data["price"], 
                    data["barcode"],
                    token,
                    esl_ip
                )
                return response
            except ClientResponseError as e:
                print(f"Error sending to ESL: {e}")


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
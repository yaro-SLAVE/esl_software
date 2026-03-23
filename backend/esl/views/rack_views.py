from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models.company import *
from esl.models.rack import *
from esl.models.esl import *
from esl.models.profile import *

from esl.serializers.rack_serializers import *

from aiohttp import ClientSession, ClientResponseError
from django.http import Http404

from rest_framework import serializers

from rest_framework.response import Response

from esl.onec_esl.api.product import send_product, ESLResponse

import asyncio

from esl.onec_1c.services import get_products_list, get_product_info, get_updates

from dataclasses import asdict


class RackViewset(
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    class ESLSerializer(serializers.Serializer):
        name = serializers.CharField()
        price = serializers.FloatField()
        barcode = serializers.CharField()

    queryset=Rack.objects.all()
    permission_classes=[IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "update":
            return RackUpdateSerializer
        elif self.action == "list":
            return RackListSerializer
        else: 
            return RackSerializer
        
    def list(self, request, *args, **kwargs):
        filial_id = request.GET.get('filial') 
        filial = CompanyFilial.objects.filter(pk=filial_id).first()

        racks = self.get_queryset().filter(filial=filial)

        response = {
            "filial": {
                "name": filial.name,
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
                        "external_id": product.external_id,
                        "short_name": product.short_name,
                        "shelf": product.shelf,
                        "number": product.number
                    } for product in products
                ]
            })
        
        serializer = self.get_serializer(response)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        r = super().update(request, *args, **kwargs)

        # if ("products" in request.data):
        #     pk = self.kwargs["pk"]

        #     rack = Rack.objects.filter(pk=pk).first()

        #     product = Product.objects.filter(rack = rack).first()

        #     serializer = self.ESLSerializer(data={
        #         'name': product.short_name,
        #         'price': product.price,
        #         'barcode': product.barcode
        #     })
        #     serializer.is_valid(raise_exception=True)

        #     esl = ESL.objects.filter(rack = rack).first()

        #     asyncio.run(self.send_to_esl(
        #                 serializer.validated_data,
        #                 esl.token,
        #                 esl.esl_ip
        #             ))
                
        return r

    # async def send_to_esl(self, data, token, esl_ip):
    #     async with ClientSession() as client:
    #         try:
    #             response = await send_product(
    #                 client, 
    #                 data["name"], 
    #                 data["price"], 
    #                 data["barcode"],
    #                 token,
    #                 esl_ip
    #             )
    #             return response
    #         except ClientResponseError as e:
    #             print(f"Error sending to ESL: {e}")
    
    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]

        rack = Rack.objects.get(pk=pk)
        rack.row = -1
        rack.column = -1
        rack.save()

        return Response()


class ProductViewset(
    ListModelMixin,
    GenericViewSet
):
    queryset=Product.objects.all()
    permission_classes=[IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'show_product':
            return ProductShowSerializer
        elif self.action == 'products_update':
            return UpdateProductSerializer
        elif self.action == 'list':
            return ProductSerializer
        else:
            return ProductSerializer
   
    def list(self, request, *args, **kwargs):
        # userprofile = UserProfile.objects.filter(user = self.request.user).first()
        products = []
        try:
            products_list = get_products_list('')
            products_list = asdict(products_list)

            for product_item in products_list:
                print(product_item)
                product, created = Product.objects.get_or_create(
                    external_id = product_item['id']
                )

                product.short_name = product_item['short_name']
                product.save()

                products.append(product)
        except Exception as e:
            products = Product.objects.all()
        
        serializer = self.get_serializer(products, many=True)

        return Response(data=serializer.data, status=200)

    @action(['GET'], url_path="show", detail=False)
    def show_product(self, request): 
        company_id = request.GET.get('company', None)
        product_id = request.GET.get('product', None)
        # company = Company.objects.filter(pk = company_id).first()

        product_info = get_product_info('', product_id)

        serializer = self.get_serializer(product_info)

        return Response(data=serializer.data, status=200)

    @action(['POST', 'GET'], url_path="update", detail=False)
    def products_update(self, request, *args, **kwargs):
        if request.method == 'POST':
            updates = request.data['updates']
        else:
            updates = get_updates('')
            updates = [ asdict(update) for update in updates]

        if len(updates) > 0:
            for update in updates:
                product = Product.objects.filter(external_id = update['id']).first()

                if product is not None:
                    data = {
                        "company": 1,
                        "product": product.pk,
                        "price": update['price'],
                        "short_name": update['short_name']
                    }

                    if 'promotion' in update:
                        data['promotion'] = update['promotion']
                    if 'have_promotion' in update:
                        data['have_promotion'] = update['have_promotion']

                    esl = ESL.objects.filter(rack = product.rack).first()

                    if (product.pk == 3):
                        asyncio.run(self.send_to_esl(
                            data,
                            'qwe123123qwe', #esl.token,
                            '10.35.41.216', #esl.esl_ip
                        ))
                
        return Response(200)
    
    # @action(['GET'], url_path="update", detail=False)
    # def products_update_force(self, request, *args, **kwargs):
    #     updates = get_updates('')

    #     if len(updates) > 0:
    #         for update in updates:
    #             product = Product.objects.filter(external_id = update['id']).first()

    #             if product is not None:
    #                 data = {
    #                     "company": 1,
    #                     "product": product.pk,
    #                     "price": update['price'],
    #                     "short_name": update['short_name']
    #                 }

    #                 if 'promotion' in update:
    #                     data['promotion'] = update['promotion']
    #                 if 'have_promotion' in update:
    #                     data['have_promotion'] = update['have_promotion']

    #                 esl = ESL.objects.filter(rack = product.rack).first()

    #                 if (product.pk == 3):
    #                     asyncio.run(self.send_to_esl(
    #                         data,
    #                         'qwe123123qwe', #esl.token,
    #                         '10.35.41.216', #esl.esl_ip
    #                     ))

    #     return Response(200)

    async def send_to_esl(self, data, token, esl_ip):
        async with ClientSession() as client:
            try:
                response = await send_product(
                    client, 
                    data,
                    token,
                    esl_ip
                )
                return response
            except ClientResponseError as e:
                print(f"Error sending to ESL: {e}")

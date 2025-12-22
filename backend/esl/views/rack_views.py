from rest_framework.decorators import action

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models import *

from esl.serializers.rack_serializers import *

class RackViewset(
    ListModelMixin,
    GenericViewSet
):
    queryset=Rack.objects.all()
    serializer_class=RackSerializer

class ProductViewset(
    ListModelMixin,
    GenericViewSet
):
    queryset=Product.objects.all()

    def get_serializer_class(self):
        if action == 'show_product':
            return ProductShowSerializer
        else:
            return ProductSerializer

    @action(['GET'], url_path=r"(?P<barcode>[a-z0-9]+)", detail=False)
    def show_product(self, request, barcode): 
        product = self.get_queryset().get(barcode=barcode)
        return product
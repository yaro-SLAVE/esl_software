from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from backend.esl.models.company import *

from esl.serializers.company_serializers import *

class CompanyViewset(
    GenericViewSet
):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer

class CompanyFilialViewset(
    GenericViewSet
):
    queryset=CompanyFilial.objects.all()
    serializer_class=CompanyFilialSerializer
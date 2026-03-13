from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models.company import *
from esl.models.rack import *
from esl.models.esl import *
from esl.models.profile import *

from esl.serializers.esl_serializers import *

from aiohttp import ClientSession, ClientResponseError
from django.http import Http404

from rest_framework import serializers

from rest_framework.response import Response

import asyncio

class ESLViewset(
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet
):
    queryset=ESL.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'create':
            return ESLCreateSerializer
        else:
            return ESLSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
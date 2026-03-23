from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models.company import *

from esl.serializers.company_serializers import *

from esl.onec_1c.services import get_filial_info, get_company_info

from esl.onec_1c.app_1c.services.k8s_service import *

import uuid

import json
from dataclasses import dataclass, asdict

class CompanyViewset(
    GenericViewSet,
    ListModelMixin
):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    permission_classes=[IsAuthenticated]

    class InnerSerializer(serializers.Serializer):
        class Info(serializers.Serializer):
            id = serializers.CharField()
            name = serializers.CharField()
        company = Info()
        filials = Info(many=True)

    def get_queryset(self):
        userprofile = UserProfile.objects.filter(user = self.request.user).first()
        return super().get_queryset().filter(pk = userprofile.company.pk).first()
    
    def list(self, request, *args, **kwargs):
        company = self.get_queryset()
        company_info = {}

        company_info = get_company_info(company.container_id)

        data = asdict(company_info)

        print(data)

        new_company, created = Company.objects.get_or_create(
            external_id = data['company']['id']
        )

        new_company.name = data['company']['name']
        new_company.save()

        data['company']['id'] = new_company.pk

        for filial in data['filials']:
            new_filial, created = CompanyFilial.objects.get_or_create(
                external_id = filial['id'],
                company = new_company
            )

            filial['id'] = new_filial.pk

            new_filial.name = filial['name']
            new_filial.save()

        return Response(data)

class CompanyFilialViewset(
    GenericViewSet,
    ListModelMixin,
    RetrieveModelMixin
):
    queryset=CompanyFilial.objects.all()
    serializer_class=CompanyFilialSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        userprofile = UserProfile.objects.filter(user = self.request.user).first()
        return super().get_queryset().filter(pk = userprofile.filial.pk).first()
    
    def list(self, request, *args, **kwargs):
        filial = self.get_queryset()
        userprofile = UserProfile.objects.filter(user = self.request.user).first()

        filial_info = get_filial_info(userprofile.company.container_id, filial.pk)

        new_filial, created = CompanyFilial.objects.get_or_create(
            external_id = filial_info['id']
        )

        new_filial.name = filial['name']
        new_filial.save()
        
        return new_filial
    
    def retrieve(self, request, *args, **kwargs):
        userprofile = UserProfile.objects.filter(user = self.request.user).first()
        filial = CompanyFilial.objects.filter(pk = kwargs.get('pk')).first()

        filial_info = asdict(get_filial_info(userprofile.company.container_id, filial.external_id))

        new_filial, created = CompanyFilial.objects.get_or_create(
            external_id = filial_info['id']
        )

        new_filial.name = filial_info['name']
        new_filial.save()

        serializer = self.get_serializer(new_filial)
        
        return Response(serializer.data)

        

class IntegrationViewset(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    UpdateModelMixin
):
    queryset=Company.objects.all()
    permission_classes=[IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return IntegrationCretaeSerializer
        else:
            return IntegrationSerializer

    # def create(self, request, *args, **kwargs):
    #     worker_id = str(uuid.uuid4())[:8]
        
    #     k8s = KubernetesService()
        
    #     deployment = k8s.create_flask_worker_deployment(worker_id)
        
    #     service = k8s.create_flask_worker_service(worker_id)
        
    #     return Response({
    #         "status": "success",
    #         "worker_id": worker_id,
    #         "deployment_name": deployment.metadata.name,
    #         "service_name": service.metadata.name,
    #         "access_url": f"http://{service.metadata.name}.default.svc.cluster.local:5000"
    #     })

    def create(self, request, *args, **kwargs):
        data = request.data
        company = userprofile = UserProfile.objects.filter(user = self.request.user).first().company

        worker_id = str(uuid.uuid4())[:8]
        company.container_id = worker_id
        company.integration_url = data['url']
        company.integration_type = data['type']

        company.save()
        return data
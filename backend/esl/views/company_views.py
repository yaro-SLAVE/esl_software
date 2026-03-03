from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models.company import *

from esl.serializers.company_serializers import *

from esl.onec_1c.services import *

from esl.onec_1c.app_1c.services.k8s_service import *

import uuid

class CompanyViewset(
    GenericViewSet,
    ListModelMixin
):
    queryset=Company.objects.all()
    serializer_class=CompanySerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        userprofile = UserProfile.objects.filter(user = self.request.user).first()
        return super().get_queryset().filter(pk = userprofile.company.pk).first()
    
    @action(detail=False, methods=['GET'], url_path='update')
    def update_company_info(self, request):
        company = self.get_queryset()
        company_info = {}

        try:
            company_info = get_company_info(company.container_id)

            new_company, created = Company.objects.get_or_create(
                external_id = company_info['company']['id']
            )

            new_company.name = company_info['company']['name']
            new_company.save()

            for filial in company_info['filials']:
                new_filial, created = CompanyFilial.objects.get_or_create(
                    external_id = filial['id']
                )

                new_filial.name = filial['name']
                new_filial.save()

            print(company_info)

            return company_info
        except Exception as e:
            print(f"error {e}")

class CompanyFilialViewset(
    GenericViewSet,
    ListModelMixin
):
    queryset=CompanyFilial.objects.all()
    serializer_class=CompanyFilialSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset()

class IntegrationViewset(
    GenericViewSet,
    CreateModelMixin
):
    queryset=Company.objects.all()
    serializer_class=IntegrationSerializer
    permission_classes=[IsAuthenticated]

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
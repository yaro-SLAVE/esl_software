from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

from esl.models.company import *

from esl.serializers.company_serializers import *

from esl.onec_1c.services import *

import uuid

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

class IntegrationViewset(
    GenericViewSet,
    CreateModelMixin
):
    queryset=Company.objects.all()
    serializer_class=IntegrationSerializer

    def create(self, request, *args, **kwargs):
        worker_id = str(uuid.uuid4())[:8]
        
        k8s = KubernetesService()
        
        deployment = k8s.create_flask_worker_deployment(worker_id)
        
        service = k8s.create_flask_worker_service(worker_id)
        
        return Response({
            "status": "success",
            "worker_id": worker_id,
            "deployment_name": deployment.metadata.name,
            "service_name": service.metadata.name,
            "access_url": f"http://{service.metadata.name}.default.svc.cluster.local:5000"
        })
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated

# from rest_framework.viewsets import GenericViewSet
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin

# from backend.esl.models.company import *

# from esl.serializers.organization_serializers import *

# class OrganizationViewset(
#     GenericViewSet
# ):
#     queryset=Organization.objects.all()
#     serializer_class=OrganizationSerializer

# class OrganizationFilialViewset(
#     GenericViewSet
# ):
#     queryset=OrganizationFilial.objects.all()
#     serializer_class=OrganizationFilialSerializer
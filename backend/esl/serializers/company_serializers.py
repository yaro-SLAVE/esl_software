from rest_framework import serializers

from esl.models.company import *
from esl.models.profile import *

from esl.serializers.auth_serializers import UserProfileSerializer

class CompanySerializer(serializers.ModelSerializer):
    administrators=serializers.SerializerMethodField()

    class Meta:
        model=Company
        fields=["id", "name"]

    def get_administrators(self, obj: Company):
        profiles = UserProfile.objects.filter(role="admin", company=obj).all()
        return UserProfileSerializer(profiles, many=True).data

class CompanyFilialSerializer(serializers.ModelSerializer):

    class Meta:
        model=CompanyFilial
        fields=["id", "name"]

class CompanyFilialUpdateSerializer(serializers.Serializer):
    rows = serializers.IntegerField()
    columns = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.rows = validated_data['rows']
        instance.columns = validated_data['columns']
        instance.save()

        return instance

class IntegrationCreateUpdateSerializer(serializers.Serializer):
    login=serializers.CharField(required=False)
    password=serializers.CharField(required=False)
    url=serializers.CharField(required=False)
    type=serializers.CharField(required=False)
    polling_frequency=serializers.IntegerField(required=False)
    start_time=serializers.TimeField(required=False)
    end_time=serializers.TimeField(required=False)

    def create(self, validated_data):
        company = userprofile = UserProfile.objects.filter(user = self.context['request'].user).first().company

        # worker_id = str(uuid.uuid4())[:8]
        # company.container_id = worker_id
        company.integration_url = validated_data['url']
        # company.integration_type = data['type']
        company.start_time = validated_data['start_time']
        company.end_time = validated_data['end_time']
        company.polling_frequency = validated_data['polling_frequency']

        company.save()
        return validated_data

    def update(self, instance, validated_data):
        if 'start_time' in validated_data:
            instance.start_time = validated_data['start_time']
        if 'end_time' in validated_data:
            instance.end_time = validated_data['end_time']
        if 'polling_frequency' in validated_data:
            instance.polling_frequency = validated_data['polling_frequency']
        if 'url' in validated_data:
            instance.integration_url = validated_data['url']
        
        instance.save()
        return validated_data
        

class IntegrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Company
        fields=['id', 'integration_type', 'integration_url', 'start_time', 'end_time', 'polling_frequency']
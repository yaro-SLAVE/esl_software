from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name=models.TextField()
    external_id=models.TextField(null=True, blank=True)
    polling_frequency=models.IntegerField(null=True, blank=True)
    container_id=models.TextField(null=True, blank=True)
    integration_type=models.TextField(null=True, blank=True)
    integration_url=models.TextField(null=True, blank=True)
    start_time=models.TimeField(null=True, blank=True)
    end_time=models.TimeField(null=True, blank=True)

class CompanyFilial(models.Model):
    company=models.ForeignKey(Company, related_name="filial_company", on_delete=models.CASCADE)
    name=models.TextField(null=True, blank=True)
    external_id=models.TextField(null=True, blank=True)
    rows=models.IntegerField(default=3)
    columns=models.IntegerField(default=3)
    local_bridge_url=models.TextField(null=True, blank=True)
    local_bridge_token=models.TextField(null=True, blank=True)
    

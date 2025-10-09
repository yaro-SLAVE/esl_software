from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    middle_name = models.TextField(null=True, blank=True)

class Organization(models.Model):
    general_manager=models.ForeignKey(User, related_name="general_manager", on_delete=models.CASCADE)
    ur_address=models.TextField()

class OrganizationFilial(models.Model):
    organization=models.ForeignKey(Organization, related_name="organization", on_delete=models.CASCADE)
    address=models.TextField()
    start_time=models.TimeField()
    end_time=models.TimeField()
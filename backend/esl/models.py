from django.db import models
from django.contrib.auth.models import User

class ProfileRole(models.Model):
    name=models.TextField()

class UserProfile(models.Model):
    user=models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

class Organization(models.Model):
    general_manager=models.ForeignKey(User, related_name="general_manager", on_delete=models.CASCADE)
    ur_address=models.TextField()
    name=models.TextField()

class Integration(models.Model):
    name=models.TextField()
    organization=models.ForeignKey(Organization, related_name="intagration_organization", on_delete=models.CASCADE)
    key=models.TextField()
    last_session=models.DateTimeField()

class OrganizationFilial(models.Model):
    organization=models.ForeignKey(Organization, related_name="filial_organization", on_delete=models.CASCADE)
    address=models.TextField()
    start_time=models.TimeField(null=True, blank=True)
    end_time=models.TimeField(null=True, blank=True)

class Rack(models.Model):
    filial=models.ForeignKey(OrganizationFilial, related_name="filial", on_delete=models.CASCADE)
    number=models.IntegerField()
    location=models.JSONField(null=True, blank=True)

class Product(models.Model):
    shelf=models.IntegerField()
    number=models.IntegerField()
    barcode=models.TextField()
    short_name=models.TextField()
    description=models.TextField()
    price=models.FloatField()
    have_promotion=models.BooleanField()
    prev_price=models.FloatField()
    photo=models.ImageField(upload_to='products/', null=True, blank=True)
    rack=models.ForeignKey(Rack, related_name="rack", on_delete=models.CASCADE)

class ESL(models.Model):
    rack=models.ForeignKey(Rack, related_name="esl_rack", on_delete=models.CASCADE)
    esl_id=models.TextField()
    

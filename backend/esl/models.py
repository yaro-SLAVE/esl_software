from django.db import models
from django.contrib.auth.models import User

class ProfileRole(models.Model):
    name=models.TextField()

class UserProfile(models.Model):
    user=models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)

class Organization(models.Model):
    general_manager=models.ForeignKey(User, related_name="general_manager", on_delete=models.CASCADE)
    ur_address=models.TextField()

class Integration(models.Model):
    organization=models.ForeignKey(Organization, related_name="intagration_organization", on_delete=models.CASCADE)
    key=models.TextField()
    last_session=models.DateTimeField()

class OrganizationFilial(models.Model):
    organization=models.ForeignKey(Organization, related_name="filial_organization", on_delete=models.CASCADE)
    address=models.TextField()
    start_time=models.TimeField()
    end_time=models.TimeField()

class Shelf(models.Model):
    filial=models.ForeignKey(OrganizationFilial, related_name="filial", on_delete=models.CASCADE)
    number=models.IntegerField()
    location=models.JSONField()

class Product(models.Model):
    number=models.IntegerField()
    barcode=models.TextField()
    shelf=models.ForeignKey(Shelf, related_name="shelf", on_delete=models.CASCADE)

class Item(models.Model):
    barcode=models.TextField()
    short_name=models.TextField()
    description=models.TextField()
    price=models.FloatField()
    have_promotion=models.BooleanField()
    prev_price=models.FloatField()

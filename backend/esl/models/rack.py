from django.db import models
from esl.models.company import CompanyFilial

class Rack(models.Model):
    filial=models.ForeignKey(CompanyFilial, related_name="filial", on_delete=models.CASCADE)
    number=models.IntegerField()
    row=models.IntegerField(default=0)
    column=models.IntegerField(default=0)
    shelfs_count=models.IntegerField(default=1)

class Product(models.Model):
    rack=models.ForeignKey(Rack, related_name="product_rack", on_delete=models.SET_NULL, null=True, blank=True)
    external_id=models.TextField(null=True, blank=True)
    short_name=models.TextField(null=True, blank=True)
    shelf=models.IntegerField(null=True, blank=True)
    number=models.IntegerField(null=True, blank=True)
from django.db import models
from datetime import datetime

class Firmware(models.Model):
    name=models.TextField(null=True, blank=True)
    file=models.FileField(null=True, blank=True)
    date_add=models.DateField(null=True, blank=True, default=datetime.now().date())
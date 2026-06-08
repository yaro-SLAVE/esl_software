from django.db import models
from esl.models.rack import Rack
from esl.models.firmware import Firmware
from datetime import datetime

class ESL(models.Model):
    rack=models.ForeignKey(Rack, related_name="esl_rack", on_delete=models.SET_NULL, null=True, blank=True)
    esl_ip=models.TextField()
    token=models.TextField()
    firmware=models.ForeignKey(Firmware, related_name="firmware", on_delete=models.SET_NULL, null=True, blank=True)

class ESLError(models.Model):
    description=models.TextField(null=True, blank=True)
    esl=models.ForeignKey(ESL, related_name="esl_error", on_delete=models.CASCADE)
    date=models.DateTimeField(null=True, blank=True, default=datetime.now())
    status=models.IntegerField(null=True, blank=True)
    channel=models.IntegerField(null=True, blank=True)

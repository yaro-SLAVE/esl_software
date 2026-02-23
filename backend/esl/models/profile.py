from django.db import models
from django.contrib.auth.models import User
from esl.models.company import Company, CompanyFilial

class UserProfile(models.Model):
    user=models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    company=models.ForeignKey(Company, related_name='company_administration', on_delete=models.SET_NULL, null=True, blank=True)
    filial=models.ForeignKey(CompanyFilial, related_name='filial_employee', on_delete=models.SET_NULL, null=True, blank=True)
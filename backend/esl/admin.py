from django.contrib import admin
from esl.models.profile import *
from esl.models.company import *
from esl.models.rack import *
from esl.models.esl import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Company)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(CompanyFilial)
class OrganizationFilialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(ESL)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(ESLError)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id']
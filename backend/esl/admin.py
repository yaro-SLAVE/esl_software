from django.contrib import admin

from esl.models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(OrganizationFilial)
class OrganizationFilialAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'address']

@admin.register(Integration)
class IntegrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'organization', 'name']

@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['id', 'filial', 'number']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'short_name']
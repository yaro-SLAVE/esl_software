from django.db import models
from django.utils import timezone
import uuid
from middleware import get_current_tenant

class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Название компании")
    subdomain = models.SlugField(unique=True, verbose_name="Поддомен")
    onec_api_url = models.URLField(verbose_name="URL OData 1С")
    onec_username = models.CharField(max_length=255, verbose_name="Логин 1С")
    onec_password = models.CharField(max_length=255, verbose_name="Пароль 1С")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    sync_interval = models.IntegerField(default=5, verbose_name="Интервал опроса (мин)")
    last_sync_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    worker_container_id = models.CharField(max_length=255, null=True, blank=True)
    worker_status = models.CharField(max_length=50, default='stopped')
    
    class Meta:
        db_table = 'tenants'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    
    def __str__(self):
        return f"{self.name} ({self.subdomain})"
    
    @property
    def queue_name(self):
        """Уникальное имя очереди для этого тенанта"""
        return f"1c_poller_{self.id.hex}"


class TenantOwnedModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, editable=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if not self.tenant_id:
            self.tenant = get_current_tenant()
        super().save(*args, **kwargs)


class TenantAwareManager(models.Manager):    
    def get_queryset(self):
        tenant = get_current_tenant()
        if tenant:
            return super().get_queryset().filter(tenant=tenant)
        return super().get_queryset()
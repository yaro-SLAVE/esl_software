from celery import shared_task
from .manager import TenantWorkerOrchestrator
from multitenant.models import Tenant
from django.utils import timezone
from datetime import timedelta

@shared_task
def sync_tenant_workers():
    orchestrator = TenantWorkerOrchestrator()
    orchestrator.sync_workers()
    return "Workers synchronized"

@shared_task
def collect_worker_metrics():
    orchestrator = TenantWorkerOrchestrator()
    tenants = Tenant.objects.filter(
        is_active=True,
        worker_container_id__isnull=False
    )
    
    metrics = []
    for tenant in tenants:
        stats = orchestrator.get_worker_stats(tenant)
        metrics.append({
            'tenant_id': str(tenant.id),
            'tenant_name': tenant.name,
            **stats
        })
    
    return f"Collected metrics for {len(metrics)} tenants"

@shared_task
def cleanup_commands():
    cutoff = timezone.now() - timedelta(days=7)
    
    deleted = PriceTagCommand.objects.filter(
        created_at__lt=cutoff,
        status__in=['success', 'failed']
    ).delete()
    
    return f"Cleaned up {deleted[0]} old commands"
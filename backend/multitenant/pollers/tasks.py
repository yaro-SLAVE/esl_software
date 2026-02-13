from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from multitenant.models import Tenant
from .onec_client import OneCPoller
from django.utils import timezone

logger = get_task_logger(__name__)

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,
    autoretry_for=(ConnectionError, TimeoutError),
)
def poll_1c_tenant(self, tenant_id: str):
    try:
        tenant = Tenant.objects.get(id=tenant_id)
        logger.info(f"Starting poll for {tenant.name}")
        
        poller = OneCPoller(tenant_id)
        count = poller.run()
        
        tenant.last_sync_at = timezone.now()
        tenant.worker_status = 'healthy'
        tenant.save()
        
        logger.info(f"Completed poll for {tenant.name}: {count} items")
        return f"Processed {count} items"
        
    except Tenant.DoesNotExist:
        logger.error(f"Tenant {tenant_id} not found")
        return "Tenant not found"
    except Exception as e:
        logger.exception(f"Poll failed for {tenant_id}")
        
        try:
            tenant = Tenant.objects.get(id=tenant_id)
            tenant.worker_status = 'failed'
            tenant.save()
        except:
            pass
        
        raise self.retry(exc=e)
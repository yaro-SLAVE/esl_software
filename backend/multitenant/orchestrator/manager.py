import docker
import json
import logging
from celery import Celery
from django.conf import settings
from multitenant.models import Tenant
from django.db.models import Q

logger = logging.getLogger(__name__)

class TenantWorkerOrchestrator:    
    def __init__(self):
        self.docker_client = docker.from_env()
        self.network_name = settings.DOCKER_NETWORK
        self.redis_url = settings.CELERY_BROKER_URL
        self.app_image = settings.WORKER_IMAGE
        
    def sync_workers(self):
        inactive_tenants = Tenant.objects.filter(
            Q(is_active=False) | 
            Q(onec_api_url__isnull=True)
        )
        
        for tenant in inactive_tenants:
            if tenant.worker_container_id:
                self.stop_worker(tenant)
        
        active_tenants = Tenant.objects.filter(
            is_active=True,
            onec_api_url__isnull=False
        )
        
        for tenant in active_tenants:
            self.ensure_worker_running(tenant)
    
    def ensure_worker_running(self, tenant: Tenant):
        if tenant.worker_container_id:
            try:
                container = self.docker_client.containers.get(
                    tenant.worker_container_id
                )
                if container.status == 'running':
                    if self._is_valid_worker(container, tenant):
                        return
                    
                container.remove(force=True)
            except docker.errors.NotFound:
                pass
        
        self.start_worker(tenant)
    
    def start_worker(self, tenant: Tenant):
        container_name = f"poller_{tenant.id.hex[:12]}"
    
        db_url = f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        
        environment = {
            'DATABASE_URL': db_url,
            'CELERY_BROKER_URL': self.redis_url,
            'DJANGO_SETTINGS_MODULE': 'config.settings.production',
            'TENANT_ID': str(tenant.id),
            'ONEC_URL': tenant.onec_api_url,
            'ONEC_USER': tenant.onec_username,
            'ONEC_PASSWORD': tenant.onec_password,
            'POLL_INTERVAL': str(tenant.sync_interval * 60),
        }
        
        container = self.docker_client.containers.run(
            image=self.app_image,
            name=container_name,
            environment=environment,
            network=self.network_name,
            command=f"celery -A config.celery worker --queues={tenant.queue_name} --concurrency=1 --loglevel=info",
            detach=True,
            restart_policy={"Name": "unless-stopped"},
            mem_limit="512m",  # Лимит памяти на тенанта
            cpu_period=100000,
            cpu_quota=50000,   # ~0.5 CPU на тенанта
            labels={
                'app': 'pricetag',
                'type': 'tenant_poller',
                'tenant_id': str(tenant.id),
                'tenant_name': tenant.name,
            }
        )
        
        tenant.worker_container_id = container.id
        tenant.worker_status = 'running'
        tenant.save()
        
        logger.info(f"Started worker for {tenant.name} in container {container.id[:12]}")
        return container
    
    def stop_worker(self, tenant: Tenant):
        """Останавливает worker тенанта"""
        if not tenant.worker_container_id:
            return
        
        try:
            container = self.docker_client.containers.get(
                tenant.worker_container_id
            )
            container.stop()
            container.remove()
            
            tenant.worker_container_id = None
            tenant.worker_status = 'stopped'
            tenant.save()
            
            logger.info(f"Stopped worker for {tenant.name}")
        except docker.errors.NotFound:
            tenant.worker_container_id = None
            tenant.worker_status = 'stopped'
            tenant.save()
    
    def _is_valid_worker(self, container, tenant: Tenant) -> bool:
        """Проверяет, что контейнер соответствует тенанту"""
        labels = container.labels
        return (
            labels.get('tenant_id') == str(tenant.id) and
            tenant.queue_name in ' '.join(container.args)
        )
    
    def get_worker_stats(self, tenant: Tenant) -> dict:
        """Получить статистику использования worker"""
        if not tenant.worker_container_id:
            return {'status': 'stopped'}
        
        try:
            container = self.docker_client.containers.get(
                tenant.worker_container_id
            )
            stats = container.stats(stream=False)
            
            return {
                'status': container.status,
                'cpu_usage': stats['cpu_stats']['cpu_usage']['total_usage'],
                'memory_usage': stats['memory_stats']['usage'],
                'memory_limit': stats['memory_stats']['limit'],
                'network_rx': stats['networks']['eth0']['rx_bytes'],
                'network_tx': stats['networks']['eth0']['tx_bytes'],
                'started_at': container.attrs['State']['StartedAt'],
            }
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
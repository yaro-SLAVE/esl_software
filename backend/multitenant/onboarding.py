from models import Tenant
from orchestrator.manager import TenantWorkerOrchestrator
import logg

class TenantOnboardingService:    
    def __init__(self):
        self.orchestrator = TenantWorkerOrchestrator()
    
    def create_tenant(self, data: dict) -> Tenant:        
        tenant = Tenant.objects.create(
            name=data['name'],
            subdomain=data['subdomain'],
            onec_api_url=data['onec_url'],
            onec_username=data['onec_username'],
            onec_password=data['onec_password'],
            sync_interval=data.get('sync_interval', 5),
            is_active=True,
        )
        
        from celery import current_app
        current_app.control.add_consumer(
            tenant.queue_name,
            destination=None,
        )
        
        self.orchestrator.start_worker(tenant)
        
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User.objects.create_user(
            username=data['admin_email'],
            email=data['admin_email'],
            password=User.objects.make_random_password(),
            tenant=tenant,
            is_tenant_admin=True,
        )
        
        self._send_welcome_email(user, tenant)
        
        logger.info(f"New tenant onboarded: {tenant.name} (ID: {tenant.id})")
        
        return tenant
    
    def deactivate_tenant(self, tenant_id: str):
        tenant = Tenant.objects.get(id=tenant_id)
        tenant.is_active = False
        tenant.save()
        
        self.orchestrator.stop_worker(tenant)
        
        from celery import current_app
        current_app.control.cancel_consumer(tenant.queue_name)
        
        logger.info(f"Tenant deactivated: {tenant.name}")
    
    def update_tenant_1c_credentials(self, tenant_id: str, **credentials):
        tenant = Tenant.objects.get(id=tenant_id)
        
        if 'onec_api_url' in credentials:
            tenant.onec_api_url = credentials['onec_api_url']
        if 'onec_username' in credentials:
            tenant.onec_username = credentials['onec_username']
        if 'onec_password' in credentials:
            tenant.onec_password = credentials['onec_password']
        
        tenant.save()
        
        self.orchestrator.stop_worker(tenant)
        self.orchestrator.start_worker(tenant)
        
        logger.info(f"1C credentials updated for {tenant.name}")
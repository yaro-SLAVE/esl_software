from threading import local
from .models import Tenant

_thread_locals = local()

def get_current_tenant():
    return getattr(_thread_locals, 'tenant', None)

def set_current_tenant(tenant):
    _thread_locals.tenant = tenant

class TenantSubdomainMiddleware:    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        host = request.get_host().split(':')[0]
        subdomain = host.split('.')[0]
        
        if subdomain in ['www', 'admin', 'app', 'api']:
            request.tenant = None
            set_current_tenant(None)
        else:
            try:
                request.tenant = Tenant.objects.get(
                    subdomain=subdomain,
                    is_active=True
                )
                set_current_tenant(request.tenant)
            except Tenant.DoesNotExist:
                request.tenant = None
                set_current_tenant(None)
        
        return self.get_response(request)


class TenantAPIMiddleware:  
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/api/v1/bridge/'):
            api_key = request.headers.get('Authorization', '')
            if api_key.startswith('Bearer '):
                token = api_key[7:]
                try:
                    store = Store.objects.get(api_key=token)
                    request.tenant = store.tenant
                    set_current_tenant(store.tenant)
                except Store.DoesNotExist:
                    pass
        
        return self.get_response(request)
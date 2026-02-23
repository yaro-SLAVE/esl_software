import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
from typing import Dict, List, Optional
import logging
from django.conf import settings
from multitenant.models import Tenant

logger = logging.getLogger(__name__)

class OneCClient:  
    def __init__(self, tenant: Tenant):
        self.tenant = tenant
        self.base_url = tenant.onec_api_url.rstrip('/')
        self.auth = HTTPBasicAuth(
            tenant.onec_username,
            tenant.onec_password
        )
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        })
    
    def get_changed_products(self, since: datetime) -> List[Dict]:
        products = []
        skip = 0
        top = 1000
        
        while True:
            url = f"{self.base_url}/Catalog_Номенклатура"
            params = {
                '$filter': f"ModifiedDate ge datetime'{since.isoformat()}'",
                '$orderby': 'ModifiedDate',
                '$top': top,
                '$skip': skip,
                '$format': 'json'
            }
            
            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                batch = data.get('value', [])
                
                products.extend(batch)
                
                if len(batch) < top:
                    break
                    
                skip += top
                
            except requests.exceptions.RequestException as e:
                logger.error(f"1C poll error for {self.tenant.name}: {e}")
                break
        
        return products
    
    def get_product_prices(self, product_refs: List[str]) -> Dict[str, float]:
        pass


class OneCPoller:    
    def __init__(self, tenant_id: str):
        self.tenant = Tenant.objects.get(id=tenant_id)
        self.onec = OneCClient(self.tenant)
    
    def run(self):
        logger.info(f"Starting poll for {self.tenant.name}")
        
        last_sync = self.tenant.last_sync_at
        if not last_sync:
            from django.utils.timezone import now
            from datetime import timedelta
            last_sync = now() - timedelta(days=7)
        
        products_data = self.onec.get_changed_products(last_sync)
        logger.info(f"Found {len(products_data)} changed products")
        
        from django.db import transaction
        
        with transaction.atomic():
            for item in products_data:
                price = self._extract_price(item)
                
                product, created = Product.objects.update_or_create(
                    tenant=self.tenant,
                    external_id=item['Ref_Key'],
                    defaults={
                        'name': item.get('Description', ''),
                        'code': item.get('Code', ''),
                        'barcode': item.get('Штрихкод', ''),
                        'price': price,
                        'unit': item.get('Unit', 'шт'),
                        'is_active': not item.get('DeletionMark', False),
                        'modified_in_1c': item.get('ModifiedDate'),
                    }
                )
                
                if not created and product.price != price:
                    self._create_price_update_tasks(product, price)
        
        from django.utils.timezone import now
        self.tenant.last_sync_at = now()
        self.tenant.save()
        
        logger.info(f"Poll completed for {self.tenant.name}")
        return len(products_data)
    
    def _extract_price(self, item: Dict) -> float:
        if 'Цена' in item:
            return float(item['Цена'])
        elif 'Price' in item:
            return float(item['Price'])
        else:
            return 0.0
    
    def _create_price_update_tasks(self, product, new_price):        
        stores = Store.objects.filter(
            tenant=self.tenant,
            assortment__products=product
        )
        
        for store in stores:
            PriceTagCommand.objects.create(
                tenant=self.tenant,
                store=store,
                command_type='update_price',
                payload={
                    'esl_mac': product.esl_mac,
                    'product_id': str(product.id),
                    'product_name': product.name,
                    'new_price': str(new_price),
                    'old_price': str(product.price),
                }
            )
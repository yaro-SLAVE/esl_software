# import requests
from onec_1c.dataclasses import *
import requests

def get_worker_url(worker_id: str):
    #return f"http://flask-worker-{worker_id}.default.svc.cluster.local:5000"
    return "127.0.0.1:5000" # For tests

def get_products_list(worker_id: str) -> list[ProductsListItemResponse]:
    worker_url = get_worker_url(worker_id)

    r = requests.get(f"{worker_url}/api/product/")
    r.raise_for_status()
    return list[ProductsListItemResponse].schema().load(r.json())

async def get_product_info(worker_id: str, product_id: str) -> ProductInfoResponse:
    worker_url = get_worker_url(worker_id)
    
    r = requests.get(f"{worker_url}/api/product/{product_id}/")
    r.raise_for_status()
    return ProductInfoResponse.schema().load(r.json())

def get_company_info(worker_id: str) -> CompanyInfoResponse:
    worker_url = get_worker_url(worker_id)
    
    r = requests.get(f"{worker_url}/api/company-info/")
    
    return CompanyInfoResponse.schema().load(r.json())
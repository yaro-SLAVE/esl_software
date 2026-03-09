# import requests
from esl.onec_1c.dataclasses import *
import requests
from marshmallow_dataclass import class_schema

def get_worker_url(worker_id: str):
    #return f"http://flask-worker-{worker_id}.default.svc.cluster.local:5000"
    return "http://127.0.0.1:5000" # For tests

def get_products_list(worker_id: str) -> list[ProductsListItemResponse]:
    worker_url = get_worker_url(worker_id)

    r = requests.get(f"{worker_url}/api/product/")
    r.raise_for_status()
    ProductsListSchema = class_schema(ProductsListItemResponse)(many=True)
    return ProductsListSchema.load(r.json())

def get_product_info(worker_id: str, product_id: str) -> ProductInfoResponse:
    worker_url = get_worker_url(worker_id)
    
    r = requests.get(f"{worker_url}/api/product/{product_id}/")
    r.raise_for_status()
    return ProductInfoResponse.schema().load(r.json())

def get_company_info(worker_id: str) -> CompanyInfoResponse:
    worker_url = get_worker_url(worker_id)
    
    r = requests.get(f"{worker_url}/api/company-info/")
    
    return CompanyInfoResponse.schema().load(r.json())
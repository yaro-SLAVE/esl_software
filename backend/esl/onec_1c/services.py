from app_1c.services.k8s_service import KubernetesService
import requests

class OneCService:
    def __init__(self):
        self.k8s = KubernetesService()
    
    def get_data_from_worker(self, worker_id, document_type, params):
        worker_url = f"http://flask-worker-{worker_id}.default.svc.cluster.local:5000"
        
        response = requests.get(
            f"{worker_url}/api/1c/data/{document_type}",
            params=params,
            timeout=30
        )
        
        return response.json()
    
    def get_products_list(self, worker_id):
        
        response = requests.get(
            f"http://flask-worker-{worker_id}.default.svc.cluster.local:5000/api/product",
            timeout=30
        )
        
        return response.json()
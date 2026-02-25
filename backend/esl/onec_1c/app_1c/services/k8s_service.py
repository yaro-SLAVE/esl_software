from kubernetes import client, config
import os

class KubernetesService:
    def __init__(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
        self.batch_v1 = client.BatchV1Api()

    def create_flask_worker_deployment(self, worker_id, login, password, url):        
        deployment_manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": f"flask-worker-{worker_id}",
                "namespace": "default",
                "labels": {
                    "app": "flask-worker",
                    "worker-id": str(worker_id)
                }
            },
            "spec": {
                "replicas": 1,
                "selector": {
                    "matchLabels": {
                        "app": "flask-worker",
                        "worker-id": str(worker_id)
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "flask-worker",
                            "worker-id": str(worker_id)
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "flask-worker",
                                "image": "your-registry/flask-1c-worker:latest",
                                "ports": [{"containerPort": 5000}],
                                "env": [
                                    {"name": "WORKER_ID", "value": str(worker_id)},
                                    {"name": "ONEC_URL", "value": url},
                                    {"name": "ONEC_LOGIN", "value": login},
                                    {"name": "ONC_PASSWORD", "value": password}
                                ],
                                "resources": {
                                    "requests": {
                                        "memory": "256Mi",
                                        "cpu": "250m"
                                    },
                                    "limits": {
                                        "memory": "512Mi",
                                        "cpu": "500m"
                                    }
                                }
                            }
                        ],
                        "restartPolicy": "Always"
                    }
                }
            }
        }
        
        try:
            response = self.apps_v1.create_namespaced_deployment(
                namespace="default",
                body=deployment_manifest
            )
            return response
        except client.exceptions.ApiException as e:
            if e.status == 409:
                response = self.apps_v1.patch_namespaced_deployment(
                    name=f"flask-worker-{worker_id}",
                    namespace="default",
                    body=deployment_manifest
                )
                return response
            else:
                raise

    def create_flask_worker_service(self, worker_id):    
        service_manifest = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": f"flask-worker-{worker_id}",
                "namespace": "default"
            },
            "spec": {
                "selector": {
                    "app": "flask-worker",
                    "worker-id": str(worker_id)
                },
                "ports": [
                    {
                        "port": 5000,
                        "targetPort": 5000
                    }
                ],
                "type": "ClusterIP"
            }
        }
        
        try:
            response = self.core_v1.create_namespaced_service(
                namespace="default",
                body=service_manifest
            )
            return response
        except client.exceptions.ApiException as e:
            if e.status == 409:
                response = self.core_v1.patch_namespaced_service(
                    name=f"flask-worker-{worker_id}",
                    namespace="default",
                    body=service_manifest
                )
                return response
            else:
                raise

    def delete_worker(self, worker_id):        
        self.apps_v1.delete_namespaced_deployment(
            name=f"flask-worker-{worker_id}",
            namespace="default"
        )
        
        self.core_v1.delete_namespaced_service(
            name=f"flask-worker-{worker_id}",
            namespace="default"
        )
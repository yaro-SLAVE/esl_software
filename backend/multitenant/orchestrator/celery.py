from celery import Celery
from celery.schedules import crontab

app = Celery('pricetag')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'sync-tenant-workers': {
        'task': 'orchestrator.tasks.sync_tenant_workers',
        'schedule': crontab(minute='*'),
    },
    'collect-worker-metrics': {
        'task': 'orchestrator.tasks.collect_worker_metrics',
        'schedule': crontab(minute='*/5'),
    },
    'cleanup-old-commands': {
        'task': 'orchestrator.tasks.cleanup_commands',
        'schedule': crontab(minute=0, hour='*/6'),
    },
}
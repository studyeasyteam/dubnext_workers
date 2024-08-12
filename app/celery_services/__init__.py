from app.celery_worker import celery
from app.celery_services.sample_service import background_task


celery.tasks.register(background_task)
from celery import Celery

def make_celery():
    app = Celery('worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')
    app.autodiscover_tasks(['app.services'], force=True)
    return app

celery = make_celery()

from app.celery_services.sample_service import background_task

celery.tasks.register(background_task)


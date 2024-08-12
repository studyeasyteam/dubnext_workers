from app.celery_worker import celery
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))


@celery.task
def background_task(message: str):
    import time
    time.sleep(10)  # Simulate a long task
    return f"Processed message: {message}"
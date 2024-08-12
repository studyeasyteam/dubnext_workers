
from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.celery_services import background_task

router = APIRouter()



@router.get("/sample")
def hi():
    background_task.delay()
    return "hi"



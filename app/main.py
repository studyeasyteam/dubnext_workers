from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.controllers.extraction_controller import router as ETL_router
from app.controllers.auth_controller import router as auth_router
from fastapi import FastAPI

from app.models.database import SessionLocal, engine
from app.models.models import Base

load_dotenv(dotenv_path='.env')
app = FastAPI()

Base.metadata.create_all(bind=engine)
# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




api_version = "/api/v1"

# Adding the controllers
app.include_router(auth_router, prefix=api_version+"/auth", tags=["Auth"])
app.include_router(ETL_router, prefix=api_version+"/extraction", tags=["extraction"])




origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # app settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin@192.168.0.39:5432/dd01")
    SECRET_KEY = os.getenv("SECRET_KEY", "qerrtxd")

    # Keycloak settings
    KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
    KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
    KEYCLOAK_REALM_NAME = os.getenv("KEYCLOAK_REALM_NAME")
    KEYCLOAK_CLIENT_SECRET_KEY = os.getenv("KEYCLOAK_CLIENT_SECRET_KEY")
    KEYCLOAK_MAKE_USER_USERNAME = os.getenv("KEYCLOAK_MAKE_USER_USERNAME"),  # USER with keycloak admin role
    KEYCLOAK_MAKE_USER_PASSWORD = os.getenv("KEYCLOAK_MAKE_USER_PASSWORD"),

    # AWS S3 settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_S3_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "chaand")

    # Celery configs
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    CELERY_BACKEND = os.getenv("CELERY_BACKEND", "redis://redis:6379/0")

    # OPENAI SETTINGS
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

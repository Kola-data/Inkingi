from celery import Celery
import os

broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
backend_url = broker_url

celery_app = Celery(
    "inkingi", broker=broker_url, backend=backend_url, include=["app.tasks.example"]
) 
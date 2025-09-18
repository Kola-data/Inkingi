from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "inkingi_school",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.workers.tasks.email",
        "app.workers.tasks.sms",
        "app.workers.tasks.reports",
        "app.workers.tasks.ai",
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)

# Configure periodic tasks (Celery Beat)
celery_app.conf.beat_schedule = {
    "send-pending-emails": {
        "task": "app.workers.tasks.email.send_pending_emails",
        "schedule": 60.0,  # Every minute
    },
    "generate-daily-reports": {
        "task": "app.workers.tasks.reports.generate_daily_reports",
        "schedule": 86400.0,  # Every day
    },
    "cleanup-old-notifications": {
        "task": "app.workers.tasks.cleanup.cleanup_old_notifications",
        "schedule": 3600.0,  # Every hour
    },
}
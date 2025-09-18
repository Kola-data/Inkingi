"""
Email tasks
"""
from app.core.celery import celery_app


@celery_app.task
def send_email(to_email: str, subject: str, body: str):
    """Send email task"""
    # TODO: Implement email sending logic
    print(f"Sending email to {to_email}: {subject}")
    return {"status": "sent", "to": to_email}
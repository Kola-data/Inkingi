"""
SMS tasks
"""
from app.core.celery import celery_app


@celery_app.task
def send_sms(to_phone: str, message: str):
    """Send SMS task"""
    # TODO: Implement SMS sending logic
    print(f"Sending SMS to {to_phone}: {message}")
    return {"status": "sent", "to": to_phone}
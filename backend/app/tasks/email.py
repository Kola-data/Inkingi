from celery import current_task
from app.core.celery import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

@celery_app.task
def send_email_task(recipient_email: str, subject: str, body: str, html_body: str = None):
    """Send email asynchronously"""
    try:
        if not settings.SMTP_HOST:
            print(f"Email not configured. Would send to {recipient_email}: {subject}")
            return {"status": "skipped", "reason": "Email not configured"}
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.SMTP_USERNAME
        msg['To'] = recipient_email
        
        # Add text part
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Add HTML part if provided
        if html_body:
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
        
        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return {"status": "sent", "recipient": recipient_email}
    
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@celery_app.task
def send_bulk_email_task(recipients: list, subject: str, body: str, html_body: str = None):
    """Send bulk emails asynchronously"""
    results = []
    for recipient in recipients:
        result = send_email_task.delay(recipient, subject, body, html_body)
        results.append(result)
    
    return {"status": "queued", "count": len(recipients)}
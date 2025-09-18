from celery import shared_task
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_email(to_email: str, subject: str, body: str, html_body: str = None):
    """Send email to a single recipient"""
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
        msg["To"] = to_email
        
        # Add text and HTML parts
        msg.attach(MIMEText(body, "plain"))
        if html_body:
            msg.attach(MIMEText(html_body, "html"))
        
        # Send email
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"Email sent successfully to {to_email}")
        return {"status": "success", "recipient": to_email}
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return {"status": "failed", "recipient": to_email, "error": str(e)}


@shared_task
def send_bulk_email(recipients: list, subject: str, body: str, html_body: str = None):
    """Send email to multiple recipients"""
    results = []
    for recipient in recipients:
        result = send_email.delay(recipient, subject, body, html_body)
        results.append(result)
    return {"total": len(recipients), "queued": len(results)}


@shared_task
def send_pending_emails():
    """Process pending emails from database"""
    # This would fetch pending emails from database and send them
    logger.info("Processing pending emails...")
    return {"processed": 0}
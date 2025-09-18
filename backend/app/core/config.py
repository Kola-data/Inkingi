import os
from typing import List

class Settings:
    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./inkingi.db")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "43200"))
    
    # CORS
    cors_allow_origins: List[str] = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
    
    
    # File Storage
    file_storage_bucket: str = os.getenv("FILE_STORAGE_BUCKET", "inkingi")
    file_storage_endpoint: str = os.getenv("FILE_STORAGE_ENDPOINT", "http://localhost:9000")
    file_storage_access_key: str = os.getenv("FILE_STORAGE_ACCESS_KEY", "")
    file_storage_secret_key: str = os.getenv("FILE_STORAGE_SECRET_KEY", "")
    
    # Email Configuration
    email_provider: str = os.getenv("EMAIL_PROVIDER", "smtp")
    smtp_server: str = os.getenv("SMTP_SERVER", "localhost")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    sendgrid_api_key: str = os.getenv("SENDGRID_API_KEY", "")
    
    # SMS Configuration
    sms_provider: str = os.getenv("SMS_PROVIDER", "twilio")
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    # Application Settings
    app_name: str = os.getenv("APP_NAME", "Inkingi Smart School")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings() 
"""
Configuration settings for the Legal Strategy Infographics Platform.
"""

from typing import Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: Optional[str] = Field(default=None, env="DATABASE_URL")
    pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    pool_recycle: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    
    class Config:
        env_prefix = "DATABASE_"


class RedisSettings(BaseSettings):
    """Redis configuration settings."""
    
    url: Optional[str] = Field(default=None, env="REDIS_URL")
    pool_size: int = Field(default=10, env="REDIS_POOL_SIZE")
    socket_timeout: int = Field(default=5, env="REDIS_SOCKET_TIMEOUT")
    socket_connect_timeout: int = Field(default=5, env="REDIS_SOCKET_CONNECT_TIMEOUT")
    
    class Config:
        env_prefix = "REDIS_"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: Optional[str] = Field(default=None, env="SECRET_KEY")
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    mfa_required: bool = Field(default=True, env="MFA_REQUIRED")
    password_min_length: int = Field(default=12, env="PASSWORD_MIN_LENGTH")
    max_login_attempts: int = Field(default=5, env="MAX_LOGIN_ATTEMPTS")
    lockout_duration_minutes: int = Field(default=15, env="LOCKOUT_DURATION_MINUTES")
    
    @validator("secret_key")
    def validate_secret_key(cls, v: str) -> str:
        if v and len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    class Config:
        env_prefix = "SECURITY_"


class EmailSettings(BaseSettings):
    """Email configuration settings."""
    
    host: Optional[str] = Field(default=None, env="SMTP_HOST")
    port: int = Field(default=587, env="SMTP_PORT")
    username: Optional[str] = Field(default=None, env="SMTP_USER")
    password: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    use_tls: bool = Field(default=True, env="SMTP_USE_TLS")
    from_email: Optional[str] = Field(default=None, env="SMTP_FROM_EMAIL")
    
    class Config:
        env_prefix = "SMTP_"


class StorageSettings(BaseSettings):
    """File storage configuration settings."""
    
    backend: str = Field(default="local", env="STORAGE_BACKEND")
    local_path: str = Field(default="./uploads", env="STORAGE_LOCAL_PATH")
    aws_access_key_id: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    aws_bucket_name: Optional[str] = Field(default=None, env="AWS_BUCKET_NAME")
    aws_region: str = Field(default="us-east-1", env="AWS_REGION")
    max_file_size_mb: int = Field(default=50, env="STORAGE_MAX_FILE_SIZE_MB")
    
    @validator("backend")
    def validate_backend(cls, v: str) -> str:
        if v not in ["local", "s3"]:
            raise ValueError("Storage backend must be 'local' or 's3'")
        return v
    
    class Config:
        env_prefix = "STORAGE_"


class MonitoringSettings(BaseSettings):
    """Monitoring and logging configuration settings."""
    
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    sentry_dsn: Optional[str] = Field(default=None, env="SENTRY_DSN")
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    @validator("log_level")
    def validate_log_level(cls, v: str) -> str:
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    class Config:
        env_prefix = "MONITORING_"


class Settings(BaseSettings):
    """Main application settings."""
    
    # Application
    app_name: str = Field(default="Legal Strategy Infographics", env="APP_NAME")
    debug: bool = Field(default=False, env="DEBUG")
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    
    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    
    # Rate limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=900, env="RATE_LIMIT_WINDOW")  # 15 minutes
    
    # Sub-settings
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    email: EmailSettings = EmailSettings()
    storage: StorageSettings = StorageSettings()
    monitoring: MonitoringSettings = MonitoringSettings()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

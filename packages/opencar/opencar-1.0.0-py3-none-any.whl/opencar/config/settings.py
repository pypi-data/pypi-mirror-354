"""Application configuration and settings management."""

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation and type safety."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        protected_namespaces=(),
    )

    # Application Settings
    app_name: str = Field(default="OpenCar", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    secret_key: SecretStr = Field(
        default="your-secret-key-here", description="Application secret key"
    )

    # API Settings
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=4, description="Number of API workers")
    api_reload: bool = Field(default=False, description="Enable auto-reload")
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins",
    )

    # Database Settings
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/opencar",
        description="Database connection URL",
    )
    redis_url: str = Field(
        default="redis://localhost:6379/0", description="Redis connection URL"
    )

    # OpenAI Settings
    openai_api_key: SecretStr = Field(
        default="sk-mock-key", description="OpenAI API key"
    )
    openai_org_id: Optional[str] = Field(
        default=None, description="OpenAI organization ID"
    )
    openai_model: str = Field(
        default="gpt-4-turbo-preview", description="Default OpenAI model"
    )
    openai_temperature: float = Field(
        default=0.7, ge=0.0, le=2.0, description="Model temperature"
    )
    openai_max_tokens: int = Field(
        default=2000, ge=1, le=8192, description="Max tokens for completion"
    )
    openai_timeout: int = Field(
        default=30, ge=1, description="API timeout in seconds"
    )

    # ML Settings
    model_path: Path = Field(
        default=Path("/app/models"), description="Path to ML models"
    )
    device: str = Field(default="cuda", description="Compute device (cuda/cpu)")
    batch_size: int = Field(default=32, ge=1, description="Batch size")
    num_workers: int = Field(default=4, ge=0, description="Data loader workers")
    model_cache_size: int = Field(
        default=5, ge=1, description="Number of models to cache"
    )

    # Security Settings
    jwt_secret_key: SecretStr = Field(
        default="your-jwt-secret", description="JWT secret key"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_minutes: int = Field(
        default=30, ge=1, description="JWT expiration time"
    )
    bcrypt_rounds: int = Field(default=12, ge=4, description="Bcrypt rounds")

    # Monitoring Settings
    enable_metrics: bool = Field(default=True, description="Enable metrics")
    prometheus_port: int = Field(
        default=9090, description="Prometheus metrics port"
    )
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN")
    enable_tracing: bool = Field(default=True, description="Enable tracing")

    # Storage Settings
    s3_bucket: Optional[str] = Field(default=None, description="S3 bucket name")
    s3_region: str = Field(default="us-west-2", description="AWS region")
    upload_max_size: int = Field(
        default=100 * 1024 * 1024, description="Max upload size in bytes"
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"Invalid log level: {v}")
        return v

    @field_validator("device")
    @classmethod
    def validate_device(cls, v: str) -> str:
        """Validate compute device."""
        try:
            import torch
            if v == "cuda" and not torch.cuda.is_available():
                return "cpu"
        except ImportError:
            pass
        return v

    @property
    def database_settings(self) -> Dict[str, Any]:
        """Get database configuration."""
        return {
            "url": self.database_url,
            "echo": self.debug,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
        }

    @property
    def redis_settings(self) -> Dict[str, Any]:
        """Get Redis configuration."""
        return {
            "url": self.redis_url,
            "decode_responses": True,
            "max_connections": 50,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Kafka configuration
    kafka_bootstrap_servers: List[str] = ["localhost:9092"]
    kafka_group_id: Optional[str] = None
    kafka_enable_auto_commit: bool = True
    kafka_auto_offset_reset: str = "earliest"
    kafka_session_timeout_ms: int = 10000
    kafka_heartbeat_interval_ms: int = 3000

    # Application settings
    app_debug: bool = False
    app_log_level: str = "INFO"

    # Middleware settings
    logging_middleware_enabled: bool = True
    retry_middleware_enabled: bool = True

    # Metrics settings
    metrics_enabled: bool = False
    metrics_port: int = 8000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Global settings instance
settings = Settings()

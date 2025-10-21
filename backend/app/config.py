"""
Application Configuration
Loads settings from environment variables using Pydantic Settings
"""
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "AtlasIQ Web"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    ENVIRONMENT: str = Field(default="development", pattern="^(development|staging|production)$")
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./atlasiq.db"
    )
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_ECHO: bool = False
    
    # Redis
    REDIS_URL: RedisDsn = Field(default="redis://localhost:6379/0")
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    REDIS_SESSION_TTL: int = 86400  # 24 hours
    
    # JWT Authentication
    JWT_SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION_USE_openssl_rand_hex_32",
        min_length=32
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:5173"
    )
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = Field(default="*")
    CORS_ALLOW_HEADERS: str = Field(default="*")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = 60
    RATE_LIMIT_BURST: int = 10
    
    # Data Sources - Eurostat
    EUROSTAT_API_BASE: str = "https://ec.europa.eu/eurostat/api/dissemination"
    EUROSTAT_TIMEOUT: int = 30
    EUROSTAT_MAX_RETRIES: int = 3
    
    # Data Sources - ECB
    ECB_API_BASE: str = "https://data-api.ecb.europa.eu/service/data"
    ECB_API_KEY: Optional[str] = None
    ECB_TIMEOUT: int = 30
    
    # Data Sources - World Bank
    WORLDBANK_API_BASE: str = "https://api.worldbank.org/v2"
    WORLDBANK_TIMEOUT: int = 30
    
    # Data Sources - OECD
    OECD_API_BASE: str = "https://stats.oecd.org/restsdmx/sdmx.ashx"
    OECD_TIMEOUT: int = 30
    
    # Supported Countries (Benelux + Germany)
    SUPPORTED_COUNTRIES: List[str] = Field(default=["NL", "BE", "LU", "DE"])
    COUNTRY_NAMES: dict = Field(default={
        "NL": "Netherlands",
        "BE": "Belgium", 
        "LU": "Luxembourg",
        "DE": "Germany"
    })
    
    # Supported Sectors
    SUPPORTED_SECTORS: List[str] = Field(default=[
        "Manufacturing",
        "Wholesale & Retail",
        "Construction",
        "Professional Services",
        "IT & Communication",
        "Transportation & Logistics"
    ])
    
    # Background Jobs
    SCHEDULER_ENABLED: bool = True
    FETCH_SCHEDULE_CRON: str = "0 2 * * *"  # Daily at 2 AM
    RISK_CALC_SCHEDULE_CRON: str = "0 3 * * *"  # Daily at 3 AM
    CLEANUP_SCHEDULE_CRON: str = "0 4 * * 0"  # Weekly on Sunday at 4 AM
    
    # Caching
    CACHE_ENABLED: bool = True
    CACHE_DEFAULT_TTL: int = 3600
    CACHE_DASHBOARD_TTL: int = 1800  # 30 minutes
    CACHE_DATA_QUERY_TTL: int = 3600  # 1 hour
    
    # Export Settings
    EXPORT_MAX_ROWS: int = 100000
    EXPORT_TEMP_DIR: str = "/tmp/atlasiq_exports"
    EXPORT_EXPIRE_HOURS: int = 24
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    LOG_FILE: Optional[str] = None
    
    # Monitoring
    METRICS_ENABLED: bool = True
    METRICS_PORT: int = 9090
    SENTRY_DSN: Optional[str] = None
    
    # Feature Flags
    FEATURE_PORTFOLIO: bool = False
    FEATURE_MA_SIMULATOR: bool = False
    FEATURE_REALTIME_UPDATES: bool = True
    FEATURE_EXPORT_PDF: bool = False
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_connection(cls, v):
        """Ensure REDIS_URL is properly formatted"""
        if isinstance(v, str):
            return v
        return str(v)
    
    def get_cors_origins(self) -> list[str]:
        """Get CORS origins as list"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    def get_cors_methods(self) -> list[str]:
        """Get CORS methods as list"""
        if self.CORS_ALLOW_METHODS == "*":
            return ["*"]
        return [m.strip() for m in self.CORS_ALLOW_METHODS.split(",")]
    
    def get_cors_headers(self) -> list[str]:
        """Get CORS headers as list"""
        if self.CORS_ALLOW_HEADERS == "*":
            return ["*"]
        return [h.strip() for h in self.CORS_ALLOW_HEADERS.split(",")]
    
    def get_database_url(self) -> str:
        """Get database URL as string"""
        return str(self.DATABASE_URL)
    
    def get_redis_url(self) -> str:
        """Get Redis URL as string"""
        return str(self.REDIS_URL)
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.ENVIRONMENT == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.ENVIRONMENT == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    Using lru_cache to ensure settings are loaded only once
    """
    return Settings()


# Convenience export
settings = get_settings()

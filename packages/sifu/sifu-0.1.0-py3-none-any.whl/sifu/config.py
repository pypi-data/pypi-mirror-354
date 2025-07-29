""
Configuration settings for the Sifu application.
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic import BaseSettings, Field, PostgresDsn, validator, RedisDsn

class Settings(BaseSettings):
    """Application settings with environment variable overrides."""
    
    # Application settings
    DEBUG: bool = Field(False, env="DEBUG")
    ENVIRONMENT: str = Field("development", env="ENVIRONMENT")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    
    # API settings
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database settings
    DATABASE_URL: str = Field("sqlite:///./sifu.db", env="DATABASE_URL")
    TEST_DATABASE_URL: Optional[str] = Field(None, env="TEST_DATABASE_URL")
    
    # Redis settings
    REDIS_URL: RedisDsn = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    WEATHER_API_KEY: Optional[str] = Field(None, env="WEATHER_API_KEY")
    
    # Model paths
    MODEL_CACHE_DIR: Path = Path.home() / ".cache" / "sifu" / "models"
    
    # Language settings
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: List[str] = ["en", "es", "fr", "de", "it", "pt", "ru", "zh", "ja", "ko"]
    
    # Rate limiting
    RATE_LIApache 2.0 : str = "100/minute"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("MODEL_CACHE_DIR")
    def ensure_model_cache_dir_exists(cls, v: Path) -> Path:
        v.mkdir(parents=True, exist_ok=True)
        return v

# Create settings instance
settings = Settings()

# Create test settings for testing environment
test_settings = Settings(
    DATABASE_URL="sqlite:///:memory:",
    TEST_DATABASE_URL="sqlite:///:memory:",
    ENVIRONMENT="testing"
)

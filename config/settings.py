"""Application settings and configuration."""
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    """Application configuration from environment variables."""
    
    # Application
    app_name: str = "YouTube CEO Agent API"
    app_version: str = "2.0"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server
    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = int(os.getenv("PORT", "8000"))
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # OpenRouter API
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    model: str = os.getenv("MODEL", "google/gemini-2.5-flash")
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2048"))
    
    class Config:
        case_sensitive = False


settings = Settings()

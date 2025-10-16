from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # API Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "Product Chatbot API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "AI-powered chatbot for product inquiries"
    
    # External APIs
    DUMMYJSON_BASE_URL: str = "https://dummyjson.com"
    
    # Groq API Configuration
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.7
    GROQ_MAX_TOKENS: int = 1024
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

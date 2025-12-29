from functools import lru_cache
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    openai_api_key: str
    alpha_vantage_api_key: Optional[str] = None
    
    # LLM Configuration
    llm_model: str = "gpt-4o-mini"
    llm_streaming: bool = True
    llm_temperature: float = 0.7
    
    # Embeddings
    embedding_model: str = "text-embedding-3-small"
    
    # Database
    db_path: str = "chatbot.db"
    vector_db_path: str = "./vector_db"
    
    # File Upload
    upload_dir: str = "uploads"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list[str] = [".pdf"]
    
    # Vector Store
    vector_collection_name: str = "chat_knowledge"
    vector_search_k: int = 3
    
    # Text Splitting
    chunk_size: int = 1000
    chunk_overlap: int = 100
    
    # MCP Configuration
    mcp_expense_url: str = "https://splendid-gold-dingo.fastmcp.app/mcp"
    
    # CORS
    cors_origins: list[str] = ["*"]
    
    # Logging
    log_level: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def upload_path(self) -> Path:
        path = Path(self.upload_dir)
        path.mkdir(exist_ok=True)
        return path

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

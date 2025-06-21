import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # API Keys
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    
    # File Upload Settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "uploads")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    allowed_extensions: list = os.getenv("ALLOWED_EXTENSIONS", "pdf,docx,txt,md").split(",")
    
    # Vector Database Settings
    chroma_persist_dir: str = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
    
    # CORS Settings
    cors_origins: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
    
    # App Settings
    app_name: str = "Intelligent Document Analysis System"
    version: str = "1.0.0"
    description: str = "RAG-based document analysis using Gemini AI"
    
    # Embedding Settings
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    
    class Config:
        env_file = ".env"

settings = Settings() 
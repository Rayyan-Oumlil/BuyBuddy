from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

# Trouver le répertoire backend (parent du dossier app)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

# Debug: vérifier le chemin
if not ENV_FILE.exists():
    # Essayer avec le répertoire courant
    current_dir = Path(os.getcwd())
    if (current_dir / ".env").exists():
        ENV_FILE = current_dir / ".env"
    elif (current_dir.parent / ".env").exists():
        ENV_FILE = current_dir.parent / ".env"


class Settings(BaseSettings):
    """Application settings."""
    
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_dir: str = "data"  # Directory for SQLite database
    
    # SerperDev API
    serper_api_key: str = ""
    
    # eBay Browse API
    ebay_client_id: str = ""
    ebay_client_secret: str = ""
    
    # Best Buy API
    bestbuy_api_key: str = ""
    
    # LLM Provider Configuration
    llm_provider: str = "ollama"  # Options: ollama, deepseek, openai, anthropic
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        case_sensitive=False,
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra fields from .env (like old Google PSE keys)
    )


# Charger aussi depuis le .env directement si disponible
if ENV_FILE.exists():
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE)

settings = Settings()


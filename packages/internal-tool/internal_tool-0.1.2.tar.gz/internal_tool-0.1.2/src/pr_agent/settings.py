# pr_agent/settings.py
import os
from typing import ClassVar
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    #BASE_DIR: Path = Path(__file__).resolve().parent.parent

    METADATA_DIR: Path = Field(
        default=BASE_DIR / "internal-processed-docs" / "metadata",
        description="Where per-doc metadata JSONs live",
    )

    #METADATA_DIR: Path   = BASE_DIR / "internal-processed-docs" / "metadata"
    
    RAW_DIR: Path = Field(
        default=BASE_DIR / "internal-processed-docs" / "raw",
        description="Where raw text JSONs are written",
    )

    EMBEDDINGS_DIR: Path = Field(
        default=BASE_DIR / "internal-processed-docs" / "embeddings",
        description="Where .npy embeddings are stored",
    )

    #RAW_DIR: Path        = BASE_DIR / "internal-processed-docs" / "raw"
    #EMBEDDINGS_DIR: Path = BASE_DIR / "internal-processed-docs" / "embeddings"

    # ─── Google Drive settings ──────────────────────────────────────────────
    GDRIVE_CRED_FILE: Path = Field(
        ...,
        description="Path to your Google service-account JSON",
    )
    GDRIVE_FOLDER_ID: str = Field(
        ...,
        description="Root folder ID in Google Drive to crawl",
    )

    # ─── Notion settings ────────────────────────────────────────────────────
    NOTION_TOKEN: str = Field(
        ...,
        description="Integration token for your Notion workspace",
    )
    NOTION_ROOT_PAGE_ID: str = Field(
        ...,
        description="Root page ID in Notion to crawl",
    )
    # Secrets & IDs — no defaults here, so user *must* supply them
    # GDRIVE_CRED_FILE: Path
    # GDRIVE_FOLDER_ID: str
    # NOTION_TOKEN: str
    # NOTION_ROOT_PAGE_ID: str

    # ─── General settings ────────────────────────────────────────────────────
    GDRIVE_SCOPES: ClassVar[list[str]] = ["https://www.googleapis.com/auth/drive.readonly"]
    EMBEDDING_MODEL: ClassVar[list[str]] = "all-MiniLM-L6-v2"
    OLLAMA_BASE_URL: ClassVar[list[str]] = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    OLLAMA_MODEL_SHORT: ClassVar[list[str]] = os.getenv("OLLAMA_MODEL_SHORT", "mistral")
    EMBED_TOKEN_MODEL: ClassVar[list[str]] = os.getenv("EMBED_TOKEN_MODEL", "text-embedding-ada-002")
    TOKEN_LIMIT: ClassVar[list[str]] = int(os.getenv("TOKEN_LIMIT", "550"))
    TOP_TOPIC_COUNT: ClassVar[list[str]] = 3


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# instantiate once for import
settings = Settings()

from functools import lru_cache
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_DIR = Path(__file__).parent.parent.parent

class Security(BaseModel):
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    backend_cors_origins: list[AnyHttpUrl] = []

class Summary(BaseModel):
    model_name: str = "meta-llama/Meta-Llama-3.1-70B-Instruct"
    model_key: str

class Settings(BaseSettings):
    security: Security
    summary: Summary
    
    model_config = SettingsConfigDict(
        env_file=f"{PROJECT_DIR}/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        env_ignore_empty=True,
    )
        
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
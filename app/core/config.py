from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "PDF Interaction Backend"
    ENV: str = "development"
    DEBUG: bool = True

settings = Settings()

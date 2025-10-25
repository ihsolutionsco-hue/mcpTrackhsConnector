from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    trackhs_api_url: str
    trackhs_username: str
    trackhs_password: str
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

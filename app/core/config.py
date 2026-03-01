from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str
    database_url: str
    log_level: str = "INFO"
    secret_key: str 
    cors_origins: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_pass: str
    from_email: str
    
    class Config:
        env_file = ".env"

settings = Settings()

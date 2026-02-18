from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    env: str
    database_url: str
    log_level: str = "INFO"
    secret_key: str 

    class Config:
        env_file = ".env"

settings = Settings()

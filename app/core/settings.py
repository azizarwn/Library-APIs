from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Library Management System"
    VERSION: str = "0.0.1"


settings = Settings()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Library Management System"
    VERSION: str = "0.0.1"
    SECRET_KEY: str = "your_secret_key_here"  # Change this to a secure random key in production

    JWT_EXP_MINUTES: int = 60  # Token expiration time in minutes


settings = Settings()

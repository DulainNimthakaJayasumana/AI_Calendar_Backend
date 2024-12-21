# from pydantic_settings import BaseSettings
# import os

# class Settings(BaseSettings):
#     DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
#     GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
#     GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
#     GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback")

# settings = Settings()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/callback"

    class Config:
        env_file = ".env"  # Specify the .env file location

settings = Settings()

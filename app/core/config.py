from pydantic_settings import BaseSettings
from pydantic import BaseModel, EmailStr

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SENDER_NAME: str
    SENDER_EMAIL: EmailStr

    class Config:
        env_file = ".env"

settings = Settings()

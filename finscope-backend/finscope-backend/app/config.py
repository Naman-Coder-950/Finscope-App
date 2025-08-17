from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./finscope.db")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-secret-change-me")
    jwt_algo: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

settings = Settings()

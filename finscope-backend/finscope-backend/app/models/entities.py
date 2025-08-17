from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    points: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

    attempts: List["Attempt"] = Relationship(back_populates="user")

class QuizQuestion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    level: int = 1
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_option: str  # 'A', 'B', 'C', or 'D'

class Attempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    level: int
    score: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="attempts")

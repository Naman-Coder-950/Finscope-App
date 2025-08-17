from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select
from ..database import get_session
from ..models.entities import User
from ..services.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterIn(BaseModel):
    username: str
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.username == payload.username)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = User(username=payload.username, password_hash=hash_password(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    token = create_access_token({"sub": user.username})
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(payload: RegisterIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == payload.username)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return TokenOut(access_token=token)

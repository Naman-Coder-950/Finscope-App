from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from ..config import settings
from ..models.entities import User
from ..database import get_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algo)
    return encoded_jwt

def get_current_user(session: Session = Depends(get_session), token: str | None = None):
    # Very simple token fetch: allow token in Authorization: Bearer <token> OR query param 'token'
    from fastapi import Request
    from fastapi import Header
    async def _inner(request: Request, authorization: str | None = Header(default=None)):
        token_value = None
        if authorization and authorization.lower().startswith("bearer "):
            token_value = authorization.split(" ", 1)[1]
        if not token_value:
            token_value = request.query_params.get("token")
        if not token_value:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
        try:
            payload = jwt.decode(token_value, settings.jwt_secret, algorithms=[settings.jwt_algo])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user
    return _inner

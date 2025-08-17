from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import Session, select
from ..database import get_session
from ..models.entities import User
from ..services.auth import get_current_user

router = APIRouter(prefix="/rewards", tags=["Rewards"])

class RewardOut(dict):
    pass

@router.get("", response_model=dict)
def my_points(user=Depends(get_current_user()), session: Session = Depends(get_session)):
    return {"username": user.username, "points": user.points}

@router.get("/leaderboard", response_model=List[dict])
def leaderboard(session: Session = Depends(get_session)):
    users = session.exec(select(User).order_by(User.points.desc()).limit(10)).all()
    return [{"username": u.username, "points": u.points} for u in users]

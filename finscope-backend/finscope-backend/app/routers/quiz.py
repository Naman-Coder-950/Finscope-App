from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlmodel import Session, select
from ..database import get_session
from ..models.entities import QuizQuestion, Attempt, User
from ..services.auth import get_current_user

router = APIRouter(prefix="/quiz", tags=["Quiz"])

class QuestionOut(BaseModel):
    id: int
    level: int
    question: str
    options: List[str]

@router.get("", response_model=List[QuestionOut])
def get_questions(level: int = 1, session: Session = Depends(get_session)):
    rows = session.exec(select(QuizQuestion).where(QuizQuestion.level == level)).all()
    def to_out(q: QuizQuestion) -> QuestionOut:
        return QuestionOut(
            id=q.id, level=q.level, question=q.question,
            options=[q.option_a, q.option_b, q.option_c, q.option_d]
        )
    return [to_out(q) for q in rows]

class SubmitIn(BaseModel):
    answers: dict  # {question_id: option_letter}

class SubmitOut(BaseModel):
    score: int
    total: int
    gained_points: int
    new_total_points: int

@router.post("/submit", response_model=SubmitOut)
def submit_quiz(payload: SubmitIn, level: int = 1, user: User = Depends(get_current_user()), session: Session = Depends(get_session)):
    total = 0
    score = 0
    for qid_str, ans in payload.answers.items():
        qid = int(qid_str)
        q = session.get(QuizQuestion, qid)
        if not q or q.level != level:
            continue
        total += 1
        if ans.upper() == q.correct_option.upper():
            score += 1
    attempt = Attempt(user_id=user.id, level=level, score=score)
    session.add(attempt)
    gained = score * 10
    user.points += gained
    session.add(user)
    session.commit()
    return SubmitOut(score=score, total=total, gained_points=gained, new_total_points=user.points)

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from random import choice
from ..services.auth import get_current_user

router = APIRouter(prefix="/fraud", tags=["Fraud Simulation"])

SCENARIOS = [
    {
        "id": "OTP123",
        "message": "You receive a call asking for your OTP to avoid account blocking. Share it?",
        "options": ["Yes", "No"],
        "correct": "No",
        "explain": "Banks never ask for OTPs. Never share OTP."
    },
    {
        "id": "LINK001",
        "message": "You get an SMS to click a link to claim a prize. Open it?",
        "options": ["Open", "Ignore"],
        "correct": "Ignore",
        "explain": "This is phishing. Check official site instead."
    },
    {
        "id": "HTTPS777",
        "message": "Website shows a lock icon and HTTPS. Is it always safe?",
        "options": ["Yes, always", "No, still verify"],
        "correct": "No, still verify",
        "explain": "HTTPS helps, but scammers can also use HTTPS. Verify URL and source."
    },
]

class ScenarioOut(BaseModel):
    id: str
    message: str
    options: list[str]

@router.get("/scenario", response_model=ScenarioOut)
def get_scenario(user=Depends(get_current_user())):
    s = choice(SCENARIOS)
    return ScenarioOut(id=s["id"], message=s["message"], options=s["options"])

class AnswerIn(BaseModel):
    id: str
    answer: str

@router.post("/answer", response_model=dict)
def answer(payload: AnswerIn, user=Depends(get_current_user())):
    s = next((x for x in SCENARIOS if x["id"] == payload.id), None)
    if not s:
        return {"correct": False, "explain": "Scenario not found"}
    correct = payload.answer.strip() == s["correct"]
    return {"correct": correct, "explain": s["explain"]}

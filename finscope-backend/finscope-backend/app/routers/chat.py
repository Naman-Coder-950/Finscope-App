from fastapi import APIRouter
from pydantic import BaseModel
from ..services.ai import chat_ai

router = APIRouter(prefix="/chat", tags=["AI Chat"])

class ChatIn(BaseModel):
    message: str

@router.post("", response_model=dict)
async def chat(payload: ChatIn):
    reply = await chat_ai(payload.message)
    return {"reply": reply}

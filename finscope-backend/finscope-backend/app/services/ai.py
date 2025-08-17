from ..config import settings
import httpx

SYSTEM_PROMPT = (
    "You are FinScope, an AI finance copilot and fraud safety coach. "
    "Keep answers short, actionable, and in simple language. If the user message looks like a scam, warn them."
)

async def chat_ai(message: str) -> str:
    # Fallback simple rules if no OpenAI key
    if not settings.openai_api_key:
        lower = message.lower()
        if "otp" in lower or "password" in lower or "link" in lower or "kya" in lower:
            return "Never share OTP or passwords. Verify sender, check HTTPS lock icon, and don't click unknown links."
        if "invest" in lower:
            return "Diversify. Start with index funds or SIPs, set emergency fund first, and avoid get‑rich‑quick schemes."
        return "Track spending, make a budget (50/30/20), pay high‑interest debt first, and save before you spend."
    # If key present, call OpenAI Chat Completions API
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return "Sorry, I couldn't generate a response right now. Try again."

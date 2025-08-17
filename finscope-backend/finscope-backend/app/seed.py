from sqlmodel import Session
from .database import engine, init_db
from .models.entities import QuizQuestion

QUESTIONS = [
    # Level 1: Basics & fraud safety
    {
        "level": 1,
        "question": "What should you check before clicking a link in an SMS?",
        "option_a": "If it mentions a prize",
        "option_b": "If it says urgent",
        "option_c": "Sender and URL (HTTPS and domain)",
        "option_d": "Number of emojis",
        "correct_option": "C",
    },
    {
        "level": 1,
        "question": "Should you share your OTP with a bank representative?",
        "option_a": "Yes, if they insist",
        "option_b": "No, banks never ask for OTP",
        "option_c": "Only during work hours",
        "option_d": "If the call sounds professional",
        "correct_option": "B",
    },
    # Level 2: Personal finance
    {
        "level": 2,
        "question": "Which rule helps in budgeting income?",
        "option_a": "50/30/20 rule",
        "option_b": "10/10/80 rule",
        "option_c": "Spend first, save later",
        "option_d": "Always take loans",
        "correct_option": "A",
    },
    {
        "level": 2,
        "question": "What is a safe beginner investment approach?",
        "option_a": "Day trading with leverage",
        "option_b": "Index funds / SIPs",
        "option_c": "Unverified crypto tips",
        "option_d": "Putting all money in one stock",
        "correct_option": "B",
    },
]

def seed():
    init_db()
    with Session(engine) as session:
        # Simple insert (for demo). If you re-run, you may get duplicates; clear DB if needed.
        for q in QUESTIONS:
            item = QuizQuestion(**q)
            session.add(item)
        session.commit()
        print("Seeded quiz questions.")

if __name__ == "__main__":
    seed()

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello! FastAPI is working!"}


class SeoRequest(BaseModel):
    topic: str
    language: str = "English"


def generate_seo_mock(topic: str) -> dict:
    """Симулирует ответ Claude API — заменим на реальный вызов позже."""
    return {
        "title": f"How to {topic.title()} in 2024 (Step-by-Step Guide)",
        "description": (
            f"Want to learn {topic}? In this video, I'll show you everything "
            f"you need to know about {topic} — from basics to advanced tips. "
            f"Whether you're a beginner or already have some experience, "
            f"this guide will help you get results fast.\n\n"
            f"⏱ Timestamps:\n"
            f"0:00 — Introduction\n"
            f"1:00 — What is {topic}?\n"
            f"2:30 — Step-by-step breakdown\n"
            f"4:00 — Common mistakes\n"
            f"5:00 — Final tips\n\n"
            f"##{topic.replace(' ', '')} #tutorial #guide"
        ),
        "tags": [
            topic,
            f"{topic} tutorial",
            f"how to {topic}",
            f"{topic} for beginners",
            f"{topic} guide",
            "tutorial",
            "how to",
            "step by step",
        ],
    }


@app.post("/generate-seo")
def generate_seo(request: SeoRequest):
    result = generate_seo_mock(request.topic)
    return {
        "topic": request.topic,
        "language": request.language,
        **result,
    }

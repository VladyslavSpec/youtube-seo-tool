from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import anthropic

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


class SeoRequest(BaseModel):
    topic: str
    language: str = "English"


client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def generate_seo_claude(topic: str, language: str) -> dict:
    prompt = f"""You are a YouTube SEO expert. Generate SEO-optimized metadata for a YouTube video.

Topic: {topic}
Language: {language}

Return ONLY a JSON object with these exact keys:
- title: catchy, clickable YouTube title (max 100 chars)
- description: full YouTube description with emojis, timestamps, and hashtags (200-400 words)
- tags: array of 15 relevant search tags

JSON only, no extra text."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    import json
    text = message.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text.strip())


@app.post("/generate-seo")
def generate_seo(request: SeoRequest):
    result = generate_seo_claude(request.topic, request.language)
    return {
        "topic": request.topic,
        "language": request.language,
        **result,
    }

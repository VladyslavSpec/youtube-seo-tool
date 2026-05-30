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
    emoji_mode: str = "full"


client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


EMOJI_INSTRUCTIONS = {
    "none": "Do NOT use any emojis anywhere — no emojis in title, description, or tags.",
    "medium": "Use 2-4 emojis only in the description. No emojis in title or tags.",
    "full": "Use emojis freely in the description to make it engaging and visually appealing.",
}


def generate_seo_claude(topic: str, language: str, emoji_mode: str = "full") -> dict:
    emoji_instr = EMOJI_INSTRUCTIONS.get(emoji_mode, EMOJI_INSTRUCTIONS["full"])
    prompt = f"""Generate SEO-optimized metadata for a YouTube video about: {topic}

Detect the language of the topic above and write everything in that same language.
Emoji rule: {emoji_instr}

Return ONLY a JSON object with these exact keys:
- title: catchy, clickable YouTube title (max 100 chars)
- description: full YouTube description with timestamps and hashtags (200-400 words)
- tags: array of 15 relevant search tags

JSON only, no extra text."""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="You are a YouTube SEO expert. Detect the language of the topic and write ALL output in that same language. If the topic is in Russian, write in Russian. If in English, write in English. Never mix languages. Follow the emoji rule exactly as specified.",
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
    result = generate_seo_claude(request.topic, request.language, request.emoji_mode)
    return {
        "topic": request.topic,
        "language": request.language,
        **result,
    }

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

app = FastAPI()

@app.post("/gemini")
async def chat(request: Request):
    body = await request.json()
    print("BODY:", body)  # 👈 ЛОГ — ОЧЕНЬ ВАЖЕН

    user_question = body.get("question", "")

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {"parts": [{"text": user_question}]}
        ]
    }

    response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        try:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            answer = "Ошибка: пустой ответ от Gemini."
    else:
        print("DEBUG GEMINI ERROR:", response.text)  # 👈 Покажи ответ, если ошибка
        answer = f"Ошибка Gemini API: {response.status_code}"


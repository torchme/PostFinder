import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import Audio, OpenAI

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
PROXY_API_KEY = os.getenv("PROXY_API_KEY")

client = OpenAI(
    api_key=PROXY_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)


def chatgpt(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content


def audio2text(audio_path: str) -> str:
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file, model="whisper-1", response_format="text", language="ru"
        )
        return transcript.text

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from openai import Audio, OpenAI
from pydub import AudioSegment

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
PROXY_API_KEY = os.getenv("PROXY_API_KEY")

client = OpenAI(
    api_key=PROXY_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

logger.add(
    sys.stderr, format="{time} {level} {message}", filter="sub.module", level="INFO"
)


def chatgpt(prompt: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # Add multiple aggents to generate quastions
        messages=[
            {
                "role": "system",
                "content": "Ты умный AI чатбот в телеграм. Ты помогаешь студентам создавать красивые и понятные конспекты по видео лекциям.",
            },
            {"role": "user", "content": "Привет! Кто ты?"},
            {
                "role": "assistant",
                "content": """Привет! Я AI Student Assistant. Отправь мне видео и я создать конспект по теме видео что бы ты мог разобрать сложные моменты!\n
                """,
            },
            {"role": "user", "content": "Верни результат в MarkDown разметке" + prompt},
        ],
    )
    return chat_completion.choices[0].message.content


def audio2text(audio_path: str) -> str:
    ten_minutes = 60 * 1000

    song = AudioSegment.from_mp3(audio_path)
    first_10_minutes = song[:ten_minutes]
    # TODO: Split to minutes and save it in artifacts

    first_10_minutes.export(audio_path, format="mp3")

    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            file=audio_file, model="whisper-1", response_format="text", language="ru"
        )
        return transcript.text

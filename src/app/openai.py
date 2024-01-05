import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI


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
        # TODO: Add multiple aggents to generate quastions
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
    message_content = chat_completion.choices[0].message.content
    if message_content is None:
        raise ValueError("Ответ от API пустой или некорректный")
    return message_content

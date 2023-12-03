import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)
PROXY_API_KEY = os.getenv("PROXY_API_KEY")


def chatgpt(prompt: str) -> str:
    client = OpenAI(
        api_key=PROXY_API_KEY,
        base_url="https://api.proxyapi.ru/openai/v1",
    )
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return chat_completion.choices[0].message.content

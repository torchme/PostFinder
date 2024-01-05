import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
PROXY_API_KEY = os.getenv("PROXY_API_KEY")

import os
from pathlib import Path

from dotenv import load_dotenv

from src.config.managment import Config

env_state = os.getenv("ENV_STATE", "development")

if env_state == "docker":
    dotenv_path = Path(".env-docker")
else:
    dotenv_path = Path(".env")

load_dotenv(dotenv_path=dotenv_path)

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
CONTACT_ACCOUNT = os.getenv("CONTACT_ACCOUNT")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
PROXY_API_KEY = os.getenv("PROXY_API_KEY")

# Database data
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_PASS = os.getenv("DB_PASS")

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

CONFIG_PATH = "src/config/config.yaml"

config = Config(filename=CONFIG_PATH)
config.load_ids()

WHITELIST = config.whitelist

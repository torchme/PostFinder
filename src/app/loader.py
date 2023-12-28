from aiogram import Bot, Dispatcher
from telethon import TelegramClient

from src.config import API_HASH, API_ID, TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
client = TelegramClient("post_finder", api_id=API_ID, api_hash=API_HASH)

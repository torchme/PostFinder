import os
from aiogram import Bot, Dispatcher
from telethon import TelegramClient
from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

from src.config import API_HASH, API_ID, TELEGRAM_BOT_TOKEN, PROXY_API_KEY
from src.database.postgres_service import PostgresManager

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
client = TelegramClient(
    "sessions/post_finder.session", api_id=API_ID, api_hash=API_HASH
)

emb_fn = OpenAIEmbeddings(
    api_key=os.getenv("PROXY_API_KEY"),
    model="text-embedding-ada-002",
    base_url="https://api.proxyapi.ru/openai/v1",
)

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=PROXY_API_KEY,
    openai_api_base="https://api.proxyapi.ru/openai/v1",
)

pg_manager = PostgresManager()

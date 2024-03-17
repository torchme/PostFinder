import os
import tiktoken
from aiogram import Bot, Dispatcher
from telethon import TelegramClient
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.utils.extractor import Extractor   
from src.config import API_HASH, API_ID, TELEGRAM_BOT_TOKEN, PROXY_API_KEY
from src.database.postgres_service import PostgresManager

bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="markdown")

dp = Dispatcher()

client = TelegramClient(
    "src/artifacts/sessions/post_finder.session", api_id=API_ID, api_hash=API_HASH
)

emb_fn = OpenAIEmbeddings(
    api_key=os.getenv("PROXY_API_KEY"),
    model="text-embedding-ada-002",
    base_url="https://api.proxyapi.ru/openai/v1",
)

llm = ChatOpenAI(
    model_name="gpt-3.5-turbo-1106",
    temperature=0.7,
    api_key=PROXY_API_KEY,
    base_url="https://api.proxyapi.ru/openai/v1",
)

semantic_splitter = SemanticChunker(
    emb_fn, breakpoint_threshold_type="percentile", breakpoint_threshold_amount=90
)

extractor = Extractor(llm=llm)

encoding = tiktoken.get_encoding("cl100k_base")

pg_manager = PostgresManager()

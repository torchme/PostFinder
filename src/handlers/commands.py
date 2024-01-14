import os
import sys

# new 240113
import chromadb

import yaml
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from langchain.prompts import PromptTemplate
# from langchain.vectorstores import Chroma
# new 240114пше 
from langchain_community.vectorstores import Chroma

from langchain_community.document_loaders.csv_loader import CSVLoader
from loguru import logger
from src.app.loader import client, emb_fn, llm
from src.handlers.utils.scrapper import scrape_messages
from src.handlers.utils.validation import validate_parse_command_args

# __import__("pysqlite3")
# sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": os.path.join("..", "db.sqlite3"),
#     }
# }

router = Router()

config_path = os.path.join(sys.path[0], "src/config/config.yaml")
logger.info(config_path)


@router.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        welcome_message = config["messages"]["welcome"]

    await message.answer(welcome_message, parse_mode="markdown")


@router.message(Command(commands="parse"))
async def parse_channel(message: types.Message, command: CommandObject):
    args = command.args
    channel, context, limit, error_message = validate_parse_command_args(args)
    output_file = os.path.join(sys.path[0], f"src/artifacts/{channel}.csv")
    if error_message:
        await message.answer(error_message)
        return

    msg = await message.answer("Parsing...")

    await scrape_messages(
        client=client, channel=channel, output_file_path=output_file, limit=limit
    )

    await msg.edit_text("Similar searching...")

    loader = CSVLoader(
        file_path=output_file,
        source_column="text",
        metadata_columns=["date", "message_id"],
        csv_args={
            "delimiter": ";",
        },
    )
    data = loader.load()

    # >>> new 240113
    # сохранение chroma в файл
    # файл
    persistent_client = chromadb.PersistentClient(path=f"./chroma_db")
    # таблица
    chroma_collection = persistent_client.get_or_create_collection(
        name=channel, embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}  # l2 is the default
    )
    # вместо
    # chroma_db = Chroma.from_documents(data, emb_fn)
    # добавляем документы в коллекцию chroma_collection
    # PS: надо проверить, что data - это список 'строк'
    chroma_collection.add(
        documents=data,
        metadatas=[{"source": "local"} for _ in data],  # from online example
        ids=[f"id{i}" for i in range(len(data))]  # from online example
    )

    # теперь делаем LangChain Chroma
    chroma_db = Chroma(
        client=persistent_client,
        collection_name=channel,
        embedding_function=emb_fn
    )
    # <<< new 240113

    retriever = chroma_db.as_retriever()
    docs = retriever.get_relevant_documents(context, search_kwargs={"k": 10})
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs[::-1]])

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question", "context"],
        template="""Answer the question based on the context below. "\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:""",
    )

    prompt = QUERY_PROMPT.format(context=context_text, question=context)
    await msg.edit_text("Question: " + context + "\nAnswer: " + llm.predict(prompt))

import os
import sys

import yaml
from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from langchain.prompts import PromptTemplate

from loguru import logger
from src.app.loader import llm
from src.database.chroma import ChromaManager
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


@router.message(Command(commands="find"))
async def find_answer(message: types.Message, command: CommandObject):
    args = command.args
    channel, context, limit, error_message = validate_parse_command_args(args)

    if error_message:
        await message.answer(error_message)
        return

    msg = await message.answer("Searching...")

    chroma_manager = ChromaManager(channel=channel)

    await chroma_manager.update_collection()

    retriever = chroma_manager.collection.as_retriever()
    docs = retriever.get_relevant_documents(context, search_kwargs={"k": 10})
    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs[::-1]])

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question", "context"],
        template="""Answer the question based on the context below. "\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:""",
    )

    prompt = QUERY_PROMPT.format(context=context_text, question=context)
    await msg.edit_text("Question: " + context + "\nAnswer: " + llm.predict(prompt))

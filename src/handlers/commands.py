import asyncio
import time

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from langchain.prompts import PromptTemplate

from loguru import logger
from src.app.loader import llm, pg_manager, bot, encoding, extractor
from src.database.chroma_service import ChromaManager
from src.config import config
from src.utils.validation import validate_parse_command_args
from src.utils.filters import UnknownCommandFilter
from src.utils.markup import inline_markup_feedback
from src.utils.ui_helpers import update_loading_message
from src.utils.admin_service import send_to_admins

router = Router()


@router.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    """
    Sends a welcome message to the user and registers the user in the system if not already registered.
    Takes a message object as input.
    """
    welcome_message = config.get(['messages', 'welcome'])

    await message.answer(welcome_message)

    telegram_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""

    user_info = await bot.get_chat(telegram_id)
    bio = user_info.bio or ""

    if not await pg_manager.user_exists(telegram_id=telegram_id):
        await pg_manager.add_user(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            bio=bio,
        )
        logger.info(f"User {telegram_id} registered!")
    else:
        logger.info(f"User {telegram_id} is already registered!")

    if telegram_id not in config.whitelist:
        await send_to_admins(
            user_id=telegram_id,
            username="@" + username,
            first_name=first_name,
            last_name=last_name,
        )
        await message.answer(
            "Ваш аккаунт в статусе рассмотрения модерацией, пожалуйста, ожидайте"
        )


@router.message(Command(commands="find"))
async def find_answer(message: types.Message, command: CommandObject):
    """
    Asynchronous function for finding an answer based on the given message and command object.

    Parameters
    ----------
        message: aiogram.types.Message
            The message object.
        command: aiogram.filters.CommandObject
            The command object containing arguments.
    """
    if message.from_user.id not in config.whitelist:
        await message.answer(config.get(['messages', 'moderation']))
        return

    args = command.args
    channel, query, _, error_message = validate_parse_command_args(args)

    if error_message:
        await message.answer(error_message)
        return

    start_time = time.time()

    msg = await message.answer("👀 Ищем ответы...")
    update_task = asyncio.create_task(update_loading_message(msg))

    chroma_manager = ChromaManager(channel=channel)

    await chroma_manager.update_collection()

    retriever = chroma_manager.collection.as_retriever()
    docs = retriever.get_relevant_documents(
        extractor.add_features(query=query), search_kwargs={"k": 5}
    )

    context_text = "\n\n---\n\n".join([doc.page_content for doc in docs])
    relevant_post_urls = [
        f"[Пост {i+1}](t.me/{channel}/{doc.metadata['message_id']})"
        for i, doc in enumerate(docs)
    ][:5]

    QUERY_PROMPT = PromptTemplate(
        input_variables=["question", "context"],
        template="""Answer the question based on the context below. Use language as in question. "\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:""",
    )

    prompt = QUERY_PROMPT.format(context=context_text, question=query)

    update_task.cancel()
    msg_text = "🙋🏼‍♂️ *Ваш вопрос:*\n" + query + "\n\n🔍 *Найденный ответ:*\n"
    await msg.edit_text(msg_text)
    response = ""

    async for stream_response in llm.astream(prompt):
        response += stream_response.content
        msg_text += stream_response.content
        if (len(msg_text.split()) % 7 == 0) and len(msg_text.split()) >= 7:
            await msg.edit_text(msg_text)

    input_tokens = len(encoding.encode(prompt))
    output_tokens = len(encoding.encode(response))

    msg_text += "\n\n• " + "\n• ".join(relevant_post_urls)
    msg_text += "\n\n🔹 Чтобы продолжить, ответьте на это сообщение"

    await msg.edit_text(
        msg_text,
        reply_markup=inline_markup_feedback(message_id=msg.message_id),
        disable_web_page_preview=True,
    )

    end_time = time.time()
    execution_time = int(end_time - start_time)

    await pg_manager.add_action(
        telegram_id=message.from_user.id,
        response_id=msg.message_id,
        platform_type="telegram",
        resource_name=channel,
        prompt=prompt,
        query=query,
        response=response,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        execution_time=execution_time,
    )

    logger.info(f"Action for user {message.from_user.id} processed!")


@router.message(UnknownCommandFilter())
async def unknown_command(message: types.Message):
    await message.answer("Упс... Похоже я не знаю такой команды 😬")

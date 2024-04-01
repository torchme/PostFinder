import time
from aiogram import Router, types
from langchain.schema import HumanMessage, AIMessage
from loguru import logger

from src.app.loader import pg_manager, llm, encoding
from src.utils.filters import MessageReplyFilter
from src.utils.markup import inline_markup_feedback
from src.config import config

router = Router()


@router.message(MessageReplyFilter())
async def dialog(message: types.Message):
    """
    Asynchronous function that handles a dialog message and performs various operations on the message content and context.
    Takes a types.Message object as a parameter. Does not return anything.
    """
    if message.from_user.id not in config.whitelist:
        await message.answer(
            config.get(['no_rights'])
        )
        return

    start_time = time.time()

    previous_context = await pg_manager.get_previous_context(
        reply_to_message_id=message.reply_to_message.message_id
    )
    previous_prompt, previous_response, resource_name = (
        previous_context["prompt"],
        previous_context["response"],
        previous_context["resource_name"],
    )
    query = message.text

    messages = [
        HumanMessage(content=previous_prompt),
        AIMessage(content=previous_response),
        HumanMessage(content=f"Question: {message.text}\nAnswer:"),
    ]
    prompt = "\n".join([item.content for item in messages])
    print(prompt)

    msg_text = "🙋🏼‍♂️ *Ваш вопрос:*\n" + query + "\n\n🔍 *Найденный ответ:*\n"
    response = ""

    msg = await message.answer(msg_text)

    async for stream_response in llm.astream(messages):
        response += stream_response.content
        msg_text += stream_response.content

        if (len(msg_text.split()) % 7 == 0) and len(msg_text.split()) >= 7:
            await msg.edit_text(msg_text)

    msg_text += config.get(['messages','action_to_continue'])
    await msg.edit_text(
        msg_text,
        reply_markup=inline_markup_feedback(message_id=msg.message_id),
        disable_web_page_preview=True,
    )

    input_tokens = len(encoding.encode(prompt))
    output_tokens = len(encoding.encode(response))

    end_time = time.time()
    execution_time = int(end_time - start_time)

    await pg_manager.add_action(
        telegram_id=message.from_user.id,
        response_id=msg.message_id,
        platform_type="telegram",
        resource_name=resource_name,
        prompt=prompt,
        query=query,
        response=response,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        execution_time=execution_time,
    )

    logger.info(f"Action for user {message.from_user.id} processed!")

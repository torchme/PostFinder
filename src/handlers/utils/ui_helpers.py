import asyncio


async def update_loading_message(message):
    count = 0
    while True:
        count = (count % 3) + 1  # Изменение количества точек от 1 до 3
        await message.edit_text(f"👀 Ищем ответы{'.' * count}")
        await asyncio.sleep(0.2)


# async def typing_action(chat_id):
#     while True:
#         await bot.send_chat_action(chat_id, ChatActionSender.typing)
#         await asyncio.sleep(5)

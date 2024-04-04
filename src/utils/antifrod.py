from src.app.loader import bot
import aiogram

async def validate_channel(channel:str):
    chat_info = await bot.get_chat(channel)
    members_count = chat_info.members_count
    if members_count < 1000:
        return False
    return True
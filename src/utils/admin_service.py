from src.app.loader import bot
from src.config import config, ADMIN_CHAT_ID
from src.utils.markup import inline_markup_admin_user, inline_markup_admin_channel 


async def send_user_to_admins(user_id: int, username: str, first_name: str, last_name: str):
    if user_id not in config.whitelist:
        await bot.send_message(
            ADMIN_CHAT_ID,
            f"user_id: {user_id}\nusername: {username}\nfirst_name: {first_name}\nlast_name: {last_name}\n\nРазрешить доступ?",
            reply_markup=inline_markup_admin_user(user_id=user_id, username=username),
            parse_mode=None,
        )
    
async def send_channel_to_admins(user_id: int, channel: str):
    await bot.send_message(
        ADMIN_CHAT_ID,
        "Channel: {channel}\nДобавить в пул каналов?".format(channel=channel),
        reply_markup=inline_markup_admin_channel(channel=channel, user_id=user_id),
        parse_mode=None
    )   
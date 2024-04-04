from src.app.loader import bot
from src.config import config
from src.utils.markup import inline_markup_admin


async def send_user_to_admins(user_id: int, username: str, first_name: str, last_name: str):
    if user_id not in config.whitelist:
        await bot.send_message(
            config.admin_ids,
            f"user_id: {user_id}\nusername: {username}\nfirst_name: {first_name}\nlast_name: {last_name}\n\nРазрешить доступ?",
            reply_markup=inline_markup_admin(user_id=user_id, username=username),
            parse_mode=None,
        )

async def send_channel_to_admins(channel: str):
    if channel not in channel in config.channels:
        await bot.send_message(
            config.admin_ids,
            f"Channel: {channel}\nДобавить в пул каналов?",
            parse_mode=None,
        )
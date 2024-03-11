from src.app.loader import bot
from src.config import ADMIN_CHAT_ID, WHITELIST
from src.utils.markup import inline_markup_admin


async def send_to_admins(user_id: int, username: str, first_name: str, last_name: str):
    if user_id not in WHITELIST:
        await bot.send_message(
            ADMIN_CHAT_ID,
            f"user_id: {user_id}\nusername: {username}\nfirst_name: {first_name}\nlast_name: {last_name}\n\nРазрешить доступ?",
            reply_markup=inline_markup_admin(user_id=user_id, username=username),
            parse_mode=None,
        )

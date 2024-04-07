from typing import List, Optional, Tuple
from aiogram import types
from aiogram.filters import CommandObject
from src.config import config
from src.app.loader import bot
def validate_parse_command_args(args_str: Optional[str]):
    if not args_str:
        return (
            None,
            None,
            None,
            config.get(['messages', 'parse_error']),
        )
    args = args_str.split()
    channel = args[0].replace("@", "")
    context = " ".join(args[1:])
    limit = 100

    return channel, context, limit, ""

async def validate_add_channel_command_args(args_str: Optional[str]):
    if not args_str:
        return (
            None,
            config.get(['messages', 'errors', 'parse_channel_error']),
        )
    args = args_str.split()
    channel = args[0]
    
    try:
        await bot.get_chat(channel)
    except Exception as e:
        return None, "Channel not found"
    
    return channel, ""

def validate_id(
    message: types.Message, command: CommandObject, admin_ids: List[int]
) -> Tuple[Optional[int], str]:
    if message.from_user.id not in admin_ids:
        return None, "Access denied! You don't have rights for this"

    try:
        args = command.args
        user_id = int(args.strip())
        error_msg = ""
    except ValueError:
        user_id = None
        error_msg = "Error: User id must be an integer!"

    return user_id, error_msg

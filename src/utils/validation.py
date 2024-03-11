from typing import List, Optional, Tuple
from aiogram import types
from aiogram.filters import CommandObject


def validate_parse_command_args(args_str: Optional[str]):
    if not args_str:
        return (
            None,
            None,
            "No arguments provided.\nPlease specify the channel after the command, e.g., /parse channel_name",
        )
    args = args_str.split()
    channel = args[0].replace("@", "")
    context = " ".join(args[1:])
    limit = 100

    return channel, context, limit, ""


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

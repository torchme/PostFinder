from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from src.utils.validation import validate_id
from src.config import config

router = Router()


@router.message(Command(commands="add_user"))
async def add_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, config.admin_ids)

    if error_msg:
        await message.answer(error_msg)
        return

    if config.add_id(id_type="users", user_id=user_id):
        await message.answer(f"User {user_id} was successfully added!")
    else:
        await message.answer(f"User {user_id} is already in whitelist!")


@router.message(Command(commands="del_user"))
async def del_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, config.admin_ids)

    if error_msg:
        await message.answer(error_msg)
        return

    if config.remove_id(id_type="users", user_id=user_id):
        await message.answer(f"User {user_id} was removed")
    else:
        await message.answer("User ID not found in the whitelist.")

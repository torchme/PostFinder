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
        await message.answer(config.get(['messages', 'admin', 'add', 'success']).format(user_id))
    else:
        await message.answer(config.get(['messages', 'admin', 'add', 'fail']).format(user_id))

@router.message(Command(commands="del_user"))
async def del_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, config.admin_ids)

    if error_msg:
        await message.answer(error_msg)
        return

    if config.remove_id(id_type="users", user_id=user_id):
        await message.answer(config.get(['messages', 'admin', 'remove', 'success']).format(user_id))
    else:
        await message.answer(config.get(['messages', 'admin', 'remove', 'fail']))


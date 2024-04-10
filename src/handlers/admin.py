from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from src.app.loader import pg_manager, bot
from src.utils.validation import validate_id, validate_add_channel_command_args
from src.config import config

router = Router()


@router.message(Command(commands="add_user"))
async def add_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, config.admin_ids)
    telegram_id = message.from_user.id 
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or ""
    last_name = message.from_user.last_name or ""
    user_info = await bot.get_chat(telegram_id)
    bio = user_info.bio or ""
    if error_msg:
        await message.answer(error_msg)
        return

    if await pg_manager.user_exists(telegram_id=user_id):
        await message.answer(config.get(['messages', 'admin', 'users', 'add', 'fail']).format(user_id))
        return
    await pg_manager.add_user(telegram_id=telegram_id,username=username, first_name=first_name, last_name=last_name, bio=bio)
    await message.answer(config.get(['messages', 'admin', 'users', 'add', 'success']).format(user_id))
    
@router.message(Command(commands="del_user"))
async def del_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, config.admin_ids)

    if error_msg:
        await message.answer(error_msg)
        return

    if not user_id in config.admin_ids:
        await message.answer(config.get(['messages', 'errors', 'no_rights']))
        return
 
    if not await pg_manager.user_exists(telegram_id=message.from_user.id):
        await message.answer(config.get(['messages', 'admin', 'users', 'remove', 'fail']).format(user_id))
        return
    await pg_manager.del_user(telegram_id=message.from_user.id)
    await message.answer(config.get(['messages', 'admin', 'users', 'remove', 'success']).format(user_id))
    
    
@router.message(Command(commands="del_channel"))
async def del_channel(message: types.Message, command: CommandObject):
    args = command.args
    channel, error_msg = await validate_add_channel_command_args(args)
    user_id = message.from_user.id
    if error_msg:
        await message.answer(error_msg)
        return
    
    if not user_id in config.admin_ids:
        await message.answer(config.get(['messages', 'errors', 'no_rights']))
        return
    
    if not await pg_manager.channel_exists(channel=channel):
        await message.answer(config.get(['messages', 'admin', 'channel', 'remove', 'fail']).format(channel))
        return
    elif await pg_manager.del_channel(channel):
        await message.answer(config.get(['messages', 'admin', 'channel', 'remove', 'success']).format(channel))


@router.message(Command(commands="show_pool"))
async def show_pool(message: types.Message, command: CommandObject):
    text = ''
    result = await pg_manager.show_pool()
    for i, (channel, username) in enumerate(result):
        text+= f'{i+1}. {channel} добавил @{username}\n'
    await message.answer(text)
    
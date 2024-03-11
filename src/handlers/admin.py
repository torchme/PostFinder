from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from src.utils.validation import validate_id
from src.config import ADMIN_IDS, WHITELIST

router = Router()


@router.message(Command(commands="add_user"))
async def add_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, ADMIN_IDS)

    if error_msg:
        await message.answer(error_msg)
        return

    if user_id not in WHITELIST:
        WHITELIST.append(user_id)

        with open("src/artifacts/whitelist.txt", "a") as file:
            file.write(str(user_id) + "\n")

        await message.answer(f"User {user_id} was successfully added!")
    else:
        await message.answer(f"User {user_id} is already in whitelist!")


@router.message(Command(commands="del_user"))
async def del_user(message: types.Message, command: CommandObject):
    user_id, error_msg = validate_id(message, command, ADMIN_IDS)

    if error_msg:
        await message.answer(error_msg)
        return

    if user_id in WHITELIST:
        WHITELIST.remove(user_id)

        with open("src/artifacts/whitelist.txt", "r") as file:
            lines = file.readlines()

        with open("src/artifacts/whitelist.txt", "w") as file:
            for line in lines:
                if line.strip("\n") != str(user_id):
                    file.write(line)

        await message.answer(f"User {user_id} was removed")
    else:
        await message.answer("User ID not found in the whitelist.")

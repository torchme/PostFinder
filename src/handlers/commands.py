from pathlib import Path

import yaml
from aiogram import Router, types
from aiogram.filters import Command, CommandObject

from src.app.loader import client
from src.handlers.utils.scrapper import scrape_messages
from src.handlers.utils.validation import validate_parse_command_args

router = Router()

config_path = Path(__file__).parent.parent / "config" / "config.yaml"


@router.message(Command(commands=["start", "help"]))
async def send_welcome(message: types.Message):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        welcome_message = config["messages"]["welcome"]

    await message.answer(welcome_message, parse_mode="markdown")


@router.message(Command(commands="parse"))
async def parse_channel(message: types.Message, command: CommandObject):
    args = command.args
    channel, limit, error_message = validate_parse_command_args(args)

    if error_message:
        await message.answer(error_message)
        return

    msg = await message.answer("Parsing...")

    await scrape_messages(
        client=client, channel=channel, output_file_path=f"{channel}.csv", limit=limit
    )

    await msg.edit_text("Successfully parsed channel!")
    file_to_send = types.FSInputFile(f"{channel}.csv")
    await message.answer_document(
        document=file_to_send, caption="Here is the parsed data."
    )

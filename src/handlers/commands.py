from pathlib import Path

import yaml
from aiogram import Router
from aiogram.filters import Command

router = Router()

config_path = Path(__file__).parent.parent / "config" / "config.yaml"


@router.message(Command(commands=["start", "help"]))
async def send_welcome(message):
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        welcome_message = config["messages"]["welcome"]

    await message.answer(welcome_message, parse_mode="markdown")

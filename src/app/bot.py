# TODO: TELEGRAM BOT THERE
import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

from app import chatgpt

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["help", "start"])
async def send_welcome(message):
    await bot.reply_to(
        message,
        """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""",
    )


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    answer = chatgpt(message.text)
    await bot.reply_to(message, answer)


asyncio.run(bot.polling())

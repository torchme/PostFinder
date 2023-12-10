import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from telebot.async_telebot import AsyncTeleBot

from .openai import audio2text, chatgpt

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


# TODO: Text to yaml config, src/config/config.yaml
@bot.message_handler(commands=["help", "start"])
async def send_welcome(message):
    await bot.reply_to(
        message,
        """\
Привет! Я — *KarpovGPT*🤖, бот для помощи в обучении.
Ты можешь *задавать вопросы* и *получать ответы* на основе курсов!
А так же я могу помочь *создавать конспекты*👨‍💻!

*Команды:*
- /help - показывает эту справку
- /start - начало диалога
""",
        parse_mode="markdown",
    )


@bot.message_handler(func=lambda message: True, content_types=["video"])
async def send_video2text(message):
    try:
        # TODO: Split parts code to app.py
        # Part 1 - download video
        bot_msg = await bot.reply_to(message, "Смотрю видео... 📺")
        await bot.send_chat_action(message.chat.id, "typing")

        file_info = await bot.get_file(message.video.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        # Making directory for user like: src/artifacts/user_id/video/....mp4
        path_video = os.path.join(
            os.getcwd(),
            "src",
            "artifacts",
            f"{message.from_user.id}",
            file_info.file_path,
        )
        os.makedirs(os.path.dirname(path_video), exist_ok=True)
        with open(path_video, "wb") as new_file:
            new_file.write(downloaded_file)

        bot_msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_msg.message_id,
            text="Включаю субтитры...  📢",
        )
        await bot.send_chat_action(message.chat.id, "typing")

        # Part 2 - convert video to audio (TODO: Split parts code to app.py)
        video = VideoFileClip(path_video)  # type: ignore
        # Making directory for user like: src/artifacts/user_id/audios/....mp3
        path_audio = os.path.join(
            os.getcwd(),
            "src",
            "artifacts",
            f"{message.from_user.id}",
            "audios",
            "sound.mp3",
        )
        os.makedirs(os.path.dirname(path_audio), exist_ok=True)
        video.audio.write_audiofile(path_audio)
        bot_msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_msg.message_id,
            text="Записываю важные фрагменты... 📒",
        )
        await bot.send_chat_action(message.chat.id, "typing")

        # Part 3 - convert audio to text (TODO: Logging files, artifacts, masseges and clear cache )
        text = audio2text(path_audio)

        bot_msg = await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_msg.message_id,
            text="Оформляю конспект... 📒",
        )
        await bot.send_chat_action(message.chat.id, "typing")

        text = chatgpt(text)
        text = "*Конспект видео:* 📚\n" + text
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_msg.message_id,
            text=text,
            parse_mode="markdown",
        )
    except Exception as e:
        await bot.reply_to(message, f"Что-то пошло не так! 😢, \n {e}")


asyncio.run(bot.polling())

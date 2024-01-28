import asyncio

from aiogram.types import BotCommand
from loguru import logger

from src.app.loader import bot, dp
from src.handlers.commands import router as router_commands
from src.handlers.callbacks import router as router_callbacks
from src.handlers.dialog import router as router_dialog


class PostFinderBot:
    def __init__(self):
        dp.startup.register(self.startup_event)
        dp.shutdown.register(self.shutdown_event)

        dp.include_router(router_commands)
        dp.include_router(router_callbacks)
        dp.include_router(router_dialog)

    async def start(self):
        await dp.start_polling(bot)

    async def startup_event(self):
        bot_commands = [
            BotCommand(command="/help", description="Get info about me"),
            BotCommand(
                command="/find",
                description="Parse channel posts. Params: channel (str), limit (int)",
            ),
        ]
        await bot.set_my_commands(bot_commands)

        logger.warning("Registered commands")
        logger.warning("Bot started")

    async def shutdown_event(self):
        logger.warning("Bot stopped")


if __name__ == "__main__":
    bot_runner = PostFinderBot()
    asyncio.run(bot_runner.start())

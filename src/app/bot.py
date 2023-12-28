import asyncio

from aiogram.types import BotCommand
from loguru import logger

from src.app.loader import bot, dp
from src.handlers.commands import router as router_commands


class PostFinderBot:
    def __init__(self):
        dp.startup.register(self._startup_event)
        dp.shutdown.register(self._shutdown_event)

        dp.include_router(router_commands)

    async def start(self):
        await dp.start_polling(bot)

    async def _startup_event(self):
        bot_commands = [
            BotCommand(command="/help", description="Get info about me"),
            BotCommand(
                command="/parse",
                description="Parse channel posts. Params: channel (str), limit (int)",
            ),
        ]
        await bot.set_my_commands(bot_commands)

        logger.info("Registered commands")
        logger.info("Bot started")

    async def _shutdown_event(self):
        logger.info("Bot stopped")


if __name__ == "__main__":
    bot_runner = PostFinderBot()
    asyncio.run(bot_runner.start())

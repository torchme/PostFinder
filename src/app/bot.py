import asyncio

from aiogram.types import BotCommand
from aiogram.methods import DeleteWebhook
from loguru import logger

from src.app.loader import bot, dp
from src.handlers.commands import router as router_commands
from src.handlers.callbacks import router as router_callbacks
from src.handlers.dialog import router as router_dialog
from src.handlers.admin import router as router_admin


class PostFinderBot:
    def __init__(self):
        """
        Initializes the object and registers the startup and shutdown events.
        Also includes the specified routers for commands, callbacks, and dialog.
        """
        dp.startup.register(self.startup_event)
        dp.shutdown.register(self.shutdown_event)

        dp.include_router(router_admin)
        dp.include_router(router_commands)
        dp.include_router(router_callbacks)
        dp.include_router(router_dialog)

    async def start(self):
        """
        Starts the bot by polling the dispatcher.
        """
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)

    async def startup_event(self):
        """
        An asynchronous function to handle the startup event. It sets the bot commands and logs a warning message.
        """
        bot_commands = [
            BotCommand(command="/help", description="ℹ️ About me"),
            BotCommand(
                command="/find",
                description="🔍 Find response. Params: channel (str), query (str)",
            ),
            BotCommand(command="/account", description="🛒 Plan"),
        ]
        await bot.set_my_commands(bot_commands)

        logger.warning("Registered commands")
        logger.warning("Bot started")

    async def shutdown_event(self):
        """
        Asynchronous function to handle the shutdown event of the bot.
        """
        logger.warning("Bot stopped")


if __name__ == "__main__":
    bot_runner = PostFinderBot()
    asyncio.run(bot_runner.start())

from aiogram.filters import Filter
from aiogram.types import Message


class UnknownCommandFilter(Filter):
    def __init__(self) -> None:
        self.commands = ["/start", "/help", "/find"]

    async def __call__(self, message: Message) -> bool:
        try:
            return message.text.startswith("/") and message.text not in self.commands
        except Exception:
            return False


class MessageReplyFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.reply_to_message:
            return True
        return False

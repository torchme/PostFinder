from aiogram.filters import Filter
from aiogram.types import Message


class UnknownCommand(Filter):
    def __init__(self) -> None:
        self.commands = ["/start", "/help", "/find"]

    async def __call__(self, message: Message) -> bool:
        return message.text.startswith("/") and message.text not in self.commands

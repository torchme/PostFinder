from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


buttons = [
    InlineKeyboardButton(text="👍", callback_data="some1"),
    InlineKeyboardButton(text="👎", callback_data="some2"),
]

keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

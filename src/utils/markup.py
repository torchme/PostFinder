from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.schemas import FeedbackCallback


def inline_markup(message_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="👎",
            callback_data=FeedbackCallback(
                type="user_evaluation", message_id=str(message_id), feedback="dislike"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

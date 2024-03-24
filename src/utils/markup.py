from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.schemas import AdminCallback, FeedbackCallback


def inline_markup_feedback(message_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="👍",
            callback_data=FeedbackCallback(
                type="user_evaluation", message_id=str(message_id), feedback="like"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="👎",
            callback_data=FeedbackCallback(
                type="user_evaluation", message_id=str(message_id), feedback="dislike"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def inline_markup_admin(user_id: int, username: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="✅",
            callback_data=AdminCallback(
                type="admin", user_id=str(user_id), username=username, action="approve"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=AdminCallback(
                type="admin", user_id=str(user_id), username=username, action="dismiss"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

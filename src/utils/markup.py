from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.schemas import AdminUserCallback, AdminChannelCallback, FeedbackCallback


def inline_markup_feedback(message_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="👎",
            callback_data=FeedbackCallback(
                type="user_evaluation", message_id=str(message_id), feedback="dislike"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons], one_time_keyboard=True)


def inline_markup_admin_user(user_id: int, username: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="✅",
            callback_data=AdminUserCallback(
                type="admin_user", user_id=str(user_id), username=username, action="approve"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=AdminUserCallback(
                type="admin_user", user_id=str(user_id), username=username, action="dismiss"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons], one_time_keyboard=True)


def inline_markup_admin_channel(user_id:int, channel: str, ) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="✅",
            callback_data=AdminChannelCallback(
                type="admin_channel", channel=str(channel), user_id=str(user_id),action="approve"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="❌",
            callback_data=AdminChannelCallback(
                type="admin_channel", channel=str(channel), user_id=str(user_id), action="dismiss"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons], one_time_keyboard=True)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.utils.schemas import FeedbackCallback, PaymentCallback


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


def inline_markup_payment(chat_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="699₽ (30 запросов)",
            callback_data=PaymentCallback(
                type="payment", chat_id=str(chat_id), price="699", requests="30"
            ).pack(),
        ),
        InlineKeyboardButton(
            text="999₽ (100 запросов)",
            callback_data=PaymentCallback(
                type="payment", chat_id=str(chat_id), price="999", requests="100"
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

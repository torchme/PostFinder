from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.config import CONTACT_ACCOUNT
from src.utils.schemas import (
    FeedbackCallback,
    PaymentCallback,
    PaymentProcessingCallback,
)


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
        [
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
        ],
        [InlineKeyboardButton(text="Задать вопрос", url=CONTACT_ACCOUNT)],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def inline_markup_processing_payment(chat_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text="<< Назад",
            callback_data=PaymentProcessingCallback(
                type="payment_processing", chat_id=str(chat_id)
            ).pack(),
        ),
    ]

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

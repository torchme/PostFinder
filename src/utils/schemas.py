from aiogram.filters.callback_data import CallbackData


class FeedbackCallback(CallbackData, prefix="feedback"):
    type: str
    message_id: str
    feedback: str


class PaymentCallback(CallbackData, prefix="payment"):
    type: str
    chat_id: str
    price: str
    requests: str


class PaymentQuestionCallback(CallbackData, prefix="payment_question"):
    type: str
    chat_id: str


class PaymentProcessingCallback(CallbackData, prefix="payment_processing"):
    type: str
    chat_id: str

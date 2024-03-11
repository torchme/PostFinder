from aiogram.filters.callback_data import CallbackData


class FeedbackCallback(CallbackData, prefix="feedback"):
    type: str
    message_id: str
    feedback: str

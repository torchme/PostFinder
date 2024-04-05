from aiogram.filters.callback_data import CallbackData


class FeedbackCallback(CallbackData, prefix="feedback"):
    type: str
    message_id: str
    feedback: str


class AdminUserCallback(CallbackData, prefix="user"):
    type: str
    user_id: str
    username: str
    action: str

class AdminChannelCallback(CallbackData, prefix="channel"):
    type: str
    user_id: str
    channel: str
    action: str

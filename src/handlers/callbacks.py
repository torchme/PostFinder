from aiogram import F, Router, types

from src.app.loader import pg_manager, bot
from src.config import ADMIN_CHAT_ID, config
from src.utils.schemas import FeedbackCallback, AdminCallback

router = Router()


@router.callback_query(FeedbackCallback.filter(F.type == "user_evaluation"))
async def get_feedback(
    callback_query: types.CallbackQuery, callback_data: FeedbackCallback
):
    """
    Asynchronous function for handling user feedback.

    Parameters
    ----------
    callback_query : types.CallbackQuery
        The callback query object.
    callback_data : FeedbackCallback
        The callback data object.
    """
    await pg_manager.add_feedback(
        response_id=int(callback_data.message_id), feedback=callback_data.feedback
    )
    await callback_query.answer(callback_data.feedback)


@router.callback_query(AdminCallback.filter(F.type == "admin"))
async def admin_action(
    callback_query: types.CallbackQuery, callback_data: AdminCallback
):
    user_id = int(callback_data.user_id)
    username = callback_data.username

    if callback_data.action == "approve":
        config.add_id(id_type="users", user_id=user_id)

        await bot.send_message(
            ADMIN_CHAT_ID,
            config.get(['callback', 'approve', 'admins']).format(username=username, user_id=user_id),
            parse_mode=None,
        )
        await bot.send_message(
            int(user_id), config.get(['callback', 'approve', 'user'])
        )
    else:
        await bot.send_message(
            ADMIN_CHAT_ID,
            config.get(['callback', 'deny', 'admins']).format(username=username, user_id=user_id),

            parse_mode=None,
        )
        await bot.send_message(
            int(user_id), config.get(['callback', 'deny', 'user'])
        )

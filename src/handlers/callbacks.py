from aiogram import F, Router, types

from src.app.loader import pg_manager, bot
from src.config import ADMIN_CHAT_ID, config
from src.utils.schemas import FeedbackCallback, AdminUserCallback, AdminChannelCallback

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


@router.callback_query(AdminUserCallback.filter(F.type == "admin_user"))
async def admin_action_user(
    callback_query: types.CallbackQuery, callback_data: AdminUserCallback
):
    user_id = int(callback_data.user_id)
    username = callback_data.username

    if callback_data.action == "approve":
        config.add_id(id_type="users", user_id=user_id)
        await bot.send_message(
            ADMIN_CHAT_ID,
            config.get(['callback', 'approve', 'user','to_admins']).format(username=username, user_id=user_id),
            parse_mode=None,
        )
        await bot.send_message(
            int(user_id), config.get(['callback', 'approve','user', 'to_user'])
        )
        
        await pg_manager.add_user(telegram_id=user_id, username=username)
    else:
        await bot.send_message(
            ADMIN_CHAT_ID,
            config.get(['callback', 'deny', 'user', 'to_admins']).format(username=username, user_id=user_id),

            parse_mode=None,
        )
        await bot.send_message(
            int(user_id), config.get(['callback', 'deny', 'user', 'to_admins'])
        )



@router.callback_query(AdminChannelCallback.filter(F.type == "admin_channel"))
async def admin_action_channel(
    callback_query: types.CallbackQuery, callback_data: AdminChannelCallback
):
    user_id = int(callback_data.user_id)
    channel = callback_data.channel
    username = callback_data.username
    chat_info=await bot.get_chat(channel)
    if callback_data.action == "approve":
        await pg_manager.add_channel(
        channel=channel,
        user_id=user_id,
        username=username,
        members_count=await chat_info.get_member_count()
        )

        await bot.send_message(
            ADMIN_CHAT_ID,
            config.get(['callback', 'approve', 'channel', 'to_admins']).format(channel),
            parse_mode=None,
        )
        await bot.send_message(
            int(user_id), config.get(['callback', 'approve', 'channel', 'to_user']).format(channel)
        )
        
    else:
        await bot.send_message(
            ADMIN_CHAT_ID,
            config.get(['callback', 'deny', 'channel', 'to_admins']).format(channel),

            parse_mode=None,
        )
        await bot.send_message(
            int(user_id), config.get(['callback', 'deny', 'channel', 'to_user']).format(channel)
        )
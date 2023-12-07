import pytest
from telebot.types import Message, User, Chat, Video
from unittest.mock import AsyncMock, patch

# Импортируем вашего бота
from bot import bot, send_welcome, send_video2text

@pytest.mark.asyncio
async def test_send_welcome():
    # Создаем фиктивное сообщение
    message = Message(message_id=1, from_user=User(id=1, is_bot=False, first_name="Test"), chat=Chat(id=1, type="private"), text="/start")

    # Мокаем методы бота
    with patch.object(bot, 'reply_to', new_callable=AsyncMock) as mock_reply_to:
        await send_welcome(message)
        mock_reply_to.assert_awaited_once()

@pytest.mark.asyncio
async def test_send_video2text():
    # Создаем фиктивное видео-сообщение
    video_message = Message(message_id=2, from_user=User(id=1, is_bot=False, first_name="Test"), chat=Chat(id=1, type="private"))
    video_message.video = Video(file_id="1234", file_unique_id="abcd", width=640, height=480, duration=10)

    # Мокаем методы бота и внешние функции
    with patch.object(bot, 'reply_to', new_callable=AsyncMock) as mock_reply_to,\
         patch.object(bot, 'get_file', new_callable=AsyncMock) as mock_get_file,\
         patch.object(bot, 'download_file', new_callable=AsyncMock) as mock_download_file,\
         patch('bot.audio2text', new_callable=AsyncMock) as mock_audio2text:

        # Мокаем возвращаемые значения
        mock_get_file.return_value = AsyncMock(file_path="path/to/video.mp4")
        mock_download_file.return_value = b'video data'
        mock_audio2text.return_value = "Текст видео"

        await send_video2text(video_message)

        # Проверяем, что были вызваны нужные методы
        mock_reply_to.assert_awaited()
        mock_get_file.assert_awaited()
        mock_download_file.assert_awaited()
        mock_audio2text.assert_awaited()



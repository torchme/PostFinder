from typing import Optional
import pandas as pd
from loguru import logger
from telethon import TelegramClient


async def scrape_telegram_messages(
    client: TelegramClient, channel: str, min_id: int = 0, limit: int = 10_000
) -> Optional[pd.DataFrame]:
    """Scraping messages from telegram-channel"""
    await client.start()

    logger.info("Client for scrapping Created")
    logger.info("Scrapping...")

    result = []
    async for message in client.iter_messages(channel, limit=limit, min_id=min_id):
        try:
            message_info = {
                "message_id": message.id,
                "date": str(message.date),
                "text": message.text if message.text else "",
            }
            result.append(message_info)
        except Exception:
            logger.exception(f"Failed to parse message with id {message.id}")
            continue

    if result:
        return result
    return None

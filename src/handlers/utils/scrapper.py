import pandas as pd
from loguru import logger
from telethon import TelegramClient


async def scrape_messages(
    client: TelegramClient, channel: str, output_file_path: str, limit: int = 10_000
):
    """Scraping messages from telegram-channel"""
    await client.start()

    logger.info("Client for scrapping Created")
    logger.info("Scrapping...")

    result = []
    async for message in client.iter_messages(channel, limit=limit):
        try:
            message_info = {
                "message_id": message.id,
                "date": message.date,
                "text": message.text,
            }
            result.append(message_info)
        except Exception:
            logger.exception(f"Failed to parse message with id {message.id}")
            continue

    result_df = pd.DataFrame(result)
    result_df.to_csv(output_file_path, sep=";", index=False)

    logger.info(f"Successfully scrapped messages and saved them in {output_file_path}")

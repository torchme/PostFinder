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

    try:
        channel_data = pd.read_csv(output_file_path, sep=";", index_col=None)
        last_message_id = channel_data["message_id"].max() + 1
        logger.info(f"Last message ID found: {last_message_id}")
    except (FileNotFoundError, pd.errors.EmptyDataError):
        last_message_id = 0
        logger.info("No existing data found. Starting from the latest message.")

    result = []
    async for message in client.iter_messages(
        channel, limit=limit, min_id=last_message_id
    ):
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

    if result:
        result_df = pd.DataFrame(result)
        # Если данные уже существуют, добавляем новые данные
        if "channel_data" in locals():
            result_df = pd.concat([channel_data, result_df])
        result_df.to_csv(output_file_path, sep=";", index=False)
        logger.info(
            f"Successfully scrapped {len(result)} messages and saved them in {output_file_path}"
        )
    else:
        logger.info("No new messages to scrape.")

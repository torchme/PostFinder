from loguru import logger
from prefect import flow, task
from telethon import TelegramClient

from src.utils.scrapper import scrape_telegram_messages
from src.config import API_ID, API_HASH

CHANNELS_TO_SCRAPE = ["cryptovalerii", "KarpovCourses"]


@task
async def scrape_channels():
    """ "Scraping messages from telegram-channel"""
    async with TelegramClient(
        "src/artifacts/sessions/post_finder.session", API_ID, API_HASH
    ) as client:
        results = []
        for channel in CHANNELS_TO_SCRAPE:
            logger.info(f"Starting scrape for {channel}")
            result = await scrape_telegram_messages(client, channel, limit=10)
            results.append(result)
            logger.info(f"Completed scrape for {channel}")
        return results


@flow
async def daily_channel_scrape():
    """Initiates a daily task to scrape messages from Telegram channels"""
    logger.info("Starting the scraping process...")
    results = await scrape_channels()
    for result in results:
        print(result)


if __name__ == "__main__":
    daily_channel_scrape.serve(
        name="Daily Channel Scrape", tags=["scraping", "daily"], cron="0 0 * * *"
    )

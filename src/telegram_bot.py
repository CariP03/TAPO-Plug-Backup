from telegram import Bot
from telegram.error import TelegramError
import os

from logger import logger


async def send_backup_result(status: int):
    if status == 0:
        text = "Backup completed successfully 🟢!"
    elif status == 1:
        text = "Backup completed with warnings 🟡! Check logs for more details."
    else:
        text = "Backup completed with errors 🔴! Check logs for more details."

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if token and chat_id:
        logger.info(f"Sending message to Telegram chat.")
        # define bot
        bot = Bot(token=token)
        # send message
        try:
            async with bot:
                await bot.send_message(chat_id=chat_id, text=text)
        except TelegramError as e:
            logger.error("Failed to send message.", exc_info=e)

    else:
        logger.info('Telegram Bot not configured. No message will be sent.')

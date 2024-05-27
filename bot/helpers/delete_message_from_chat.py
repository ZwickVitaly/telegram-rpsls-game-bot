from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from settings import logger


async def try_delete_message(message: Message):
    try:
        logger.debug(f"Trying to delete message from chat: {message.chat.id}")
        await message.delete()
    except TelegramBadRequest as e:
        logger.error(f"Bot is not allowed to delete messages: {e}")

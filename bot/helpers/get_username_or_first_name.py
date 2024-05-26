from aiogram.types import Message, CallbackQuery
from settings import logger


def get_username_or_name(message: Message | CallbackQuery) -> str:
    logger.debug(f"Getting username or first_name")
    username = message.from_user.username
    if username:
        username = f"@{username}"
    else:
        username = message.from_user.first_name
    return username

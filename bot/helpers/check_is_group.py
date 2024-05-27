from aiogram.types import Message

from settings import logger


def is_group(message: Message) -> bool:
    logger.debug(f"Checking if chat is private. {message.chat.type}")
    return all((message.chat.type != "private", message.chat.type != "channel"))

from aiogram.types import Message

from helpers import is_group, try_delete_message
from messages import ONLY_GROUP_REPLY_MESSAGE, RPSLS_START_COMMAND_MESSAGE
from settings import logger


async def start_command_handler_RPSLS_BOT(message: Message):
    logger.info(f"User: {message.from_user.id} user /start command")
    await try_delete_message(message)
    if not is_group(message):
        logger.debug(f"Group only answer to user: {message.from_user.id}")
        await message.answer(ONLY_GROUP_REPLY_MESSAGE)
    else:
        logger.info(f"Chat whith user: {message.from_user.id} is group")
        await message.answer(RPSLS_START_COMMAND_MESSAGE)

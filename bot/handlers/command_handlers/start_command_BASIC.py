from aiogram.types import Message
from helpers import is_group, try_delete_message
from messages import ONLY_GROUP_REPLY_MESSAGE, HELLO_WORLD_MESSAGE
from settings import logger

async def start_command_handler_BASIC(message: Message):
    await try_delete_message(message)
    if not is_group(message):
        logger.debug(f"Chat: {message.chat.id} is not a group.")
        await message.answer(ONLY_GROUP_REPLY_MESSAGE)
    else:
        logger.debug(f"Basic /start command answer to user: {message.from_user.id}")
        await message.answer(HELLO_WORLD_MESSAGE)

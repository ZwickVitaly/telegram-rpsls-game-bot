from aiogram.types import Message
from sqlalchemy import select

from db import RPSLSStats, User, async_session
from helpers import get_username_or_name, is_group, try_delete_message
from messages import (
    ALREADY_REGISTERED_MESSAGE,
    NEW_PLAYER_REGISTER_MESSAGE,
    ONLY_GROUP_REPLY_MESSAGE,
)
from settings import logger


async def register_command_handler(message: Message):
    logger.info(f"User: {message.from_user.id} requested registration")
    await try_delete_message(message)
    if not is_group(message):
        logger.info(f"User: {message.from_user.id} is denied because of private chat")
        await message.answer(ONLY_GROUP_REPLY_MESSAGE)
    else:
        async with async_session() as session:
            async with session.begin():
                logger.debug(f"Checking if user: {message.from_user.id} is registered")
                username = get_username_or_name(message)
                user = (
                    await session.execute(
                        select(User).where(
                            User.id == message.from_user.id,
                        )
                    )
                ).scalar_one_or_none()
                if not user:
                    logger.info(f"User: {message.from_user.id} is new. Registering.")
                    register_user = User(id=message.from_user.id)
                    rpc_stats = RPSLSStats(user_id=message.from_user.id)
                    await session.merge(register_user)
                    await session.merge(rpc_stats)
                    await session.commit()
                    await message.answer(NEW_PLAYER_REGISTER_MESSAGE.format(username))
                elif not user.rpsls_active:
                    logger.info(f"User: {message.from_user.id} reactivated")
                    user.rpsls_active = True
                    await session.commit()
                    await message.answer(NEW_PLAYER_REGISTER_MESSAGE.format(username))
                else:
                    logger.info(f"User: {message.from_user.id} is already in database")
                    await message.answer(ALREADY_REGISTERED_MESSAGE.format(username))

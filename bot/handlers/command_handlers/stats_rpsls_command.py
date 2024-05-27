from aiogram.types import Message
from sqlalchemy import select

from helpers import is_group, try_delete_message, get_username_or_name
from messages import ONLY_GROUP_REPLY_MESSAGE, STATS_FOUND_MESSAGE, STATS_NOT_FOUND_MESSAGE, LOOKING_FOR_STATS_MESAGE
from settings import logger
from db import async_session, RPSLSStats
from helpers import times_plural



async def stats_rpsls_command_handler(message: Message):
    if not is_group(message):
        logger.debug(f"Chat: {message.chat.id} is not a group.")
        await message.answer(ONLY_GROUP_REPLY_MESSAGE)
    else:
        logger.info(f"User: {message.from_user.id} wants to know his stats")
        await message.answer(LOOKING_FOR_STATS_MESAGE)
        async with async_session() as session:
            with session.begin():
                username = get_username_or_name(message)
                stats_query = await session.execute(select(RPSLSStats).where(RPSLSStats.user_id == message.from_user.id))
                user_stats = stats_query.scalar_one_or_none()
                if user_stats:
                    wins_pf = times_plural(user_stats.wins)
                    losses_pf = times_plural(user_stats.losses)
                    stats_message = STATS_FOUND_MESSAGE.format(
                        username=username,
                        wins=user_stats.wins,
                        times_w=wins_pf,
                        losses=user_stats.losses,
                        times_l=losses_pf,
                    )
                    await message.answer(stats_message)
                else:
                    stats_message = STATS_NOT_FOUND_MESSAGE.format(username=username)
                    await message.answer(stats_message)
    await try_delete_message(message)

from sqlalchemy import select, update
from aiogram.types import ChatMemberUpdated

from db import async_session, Group, User, RPSLSStats
from settings import logger


async def my_chat_member_status_change_handler(message: ChatMemberUpdated):
    logger.warning(f"User: {message.from_user.id} changed bot status in chat: {message.chat.id}")
    new_status_value = message.new_chat_member.status.value

    async with async_session() as session:
        async with session.begin():
            logger.info("Looking if group is already in database")
            group = Group(id=message.chat.id, owner_id=message.from_user.id)
            query = await session.execute(select(Group).where(Group.id == group.id))
            registered_group = query.scalar_one_or_none()
            if not registered_group:
                logger.debug(f"Group: {message.chat.id} is not in database. Adding. Admin: {message.from_user.id}")
                admin = await session.execute(select(User).where(User.id == message.from_user.id))
                admin_is_user = admin.scalar_one_or_none()
                if not admin_is_user:
                    session.add(User(id=message.from_user.id))
                    session.add(RPSLSStats(user_id=message.from_user.id))
                session.add(group)
                await session.commit()

            elif registered_group.inactive and new_status_value == "member":
                logger.info(f"Group: {message.chat.id} is already in database, setting inactive=False")
                await session.execute(update(Group).where(Group.id == registered_group.id).values(inactive=False))

            else:
                logger.info(f"Group: {message.chat.id} expelled bot. Setting inactive=True")
                await session.execute(update(Group).where(Group.id == registered_group.id).values(inactive=True))

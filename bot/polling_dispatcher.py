from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.methods import DeleteWebhook
from aiogram.fsm.storage.redis import RedisStorage
from handlers import (
    register_command_handler,
    start_rpsls_command_handler,
    start_command_handler_RPSLS_BOT,
    my_chat_member_status_change_handler,
    rpsls_choice_callback_handler,
)

from dispatchers.lifespan_dispatcher import DispatcherLifespan
from lifespan.sqlalchemy_db_creation_manager import SQLAlchemyDBCreateAsyncManager
from db import engine, async_session, Base
from custom_filters import rpsls_callback_filter
from utils import redis_connection
from settings import logger, THROTTLE_TIMER, THROTTLE_RATE, BOT_TOKEN
from middleware import ThrottlingRedisMiddleware
from messages import THROTTLED_MESSAGE


logger.debug("Initializing bot instance")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

logger.debug("Initializing redis storage instance")
storage = RedisStorage(redis_connection)

logger.debug("Initializing dispatcher")
dp: Dispatcher = DispatcherLifespan(
    lifespan=SQLAlchemyDBCreateAsyncManager(
        async_db_engine=engine,
        async_db_session=async_session,
        db_base=Base
    ),
)


logger.debug("Registering ThrottlingRedisMiddleware to messages and callback query events")
dp.message.middleware(ThrottlingRedisMiddleware(
    rate_limit=THROTTLE_RATE, time_limit=THROTTLE_TIMER, redis=redis_connection, message=THROTTLED_MESSAGE)
)
dp.callback_query.middleware(ThrottlingRedisMiddleware(
    rate_limit=THROTTLE_RATE, time_limit=THROTTLE_TIMER, redis=redis_connection, message=THROTTLED_MESSAGE)
)


logger.debug("Registering bot reply functions")
dp.my_chat_member.register(my_chat_member_status_change_handler)
dp.message.register(start_command_handler_RPSLS_BOT, CommandStart())
dp.message.register(start_rpsls_command_handler, Command("start_rpsls"))
dp.message.register(register_command_handler, Command("register"))
dp.callback_query.register(rpsls_choice_callback_handler, rpsls_callback_filter)


async def main() -> None:
    logger.debug("Skipping updates")
    await bot(DeleteWebhook(drop_pending_updates=True))
    logger.debug("Initializing long polling")
    await dp.start_polling(bot, polling_timeout=10)

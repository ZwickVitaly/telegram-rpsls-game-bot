import asyncio

from aiohttp import web
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from custom_filters import rpsls_callback_filter
from dispatchers import DispatcherLifespan

from lifespan import SQLAlchemyDBCreateAsyncManager
from db import Base, async_session, engine
from settings import (
    WEBHOOK_SECRET_TOKEN,
    WEBHOOK_PATH,
    BASE_WEBHOOK_URL,
    BOT_TOKEN,
)
from middleware import ThrottlingRedisMiddleware
from utils import redis_connection
from settings import logger, THROTTLE_TIMER, THROTTLE_RATE
from messages import THROTTLED_MESSAGE
from handlers import (
    register_command_handler,
    start_command_handler_RPSLS_BOT,
    start_rpsls_command_handler,
    rpsls_choice_callback_handler,
    my_chat_member_status_change_handler,
)


dp = DispatcherLifespan(
    lifespan=SQLAlchemyDBCreateAsyncManager(db_base=Base, async_db_engine=engine, async_db_session=async_session)
)


bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

asyncio.run(bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET_TOKEN))

app = web.Application()

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

webhook_requests_handler = SimpleRequestHandler(
    dispatcher=dp,
    bot=bot,
    secret_token=BOT_TOKEN,
)

webhook_requests_handler.register(app, path=WEBHOOK_PATH)

setup_application(app, dp, bot=bot)
logger.debug("Dispatcher setup complete")

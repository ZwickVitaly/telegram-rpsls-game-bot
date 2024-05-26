from typing import Callable, Any, Awaitable

from aiogram.types import TelegramObject, Message, CallbackQuery

from aiogram import BaseMiddleware
from redis import StrictRedis

from helpers import try_delete_message, get_username_or_name

from settings import logger


class ThrottlingRedisMiddleware(BaseMiddleware):

    def __init__(
            self,
            rate_limit: int,
            time_limit: int,
            redis: StrictRedis,
            prefix: str = "throttle",
            message: str = f"Throttled",
            timeout: int = 0,
    ):
        if rate_limit <= 0 or time_limit <= 0:
            raise ValueError(
                f"Why in the name of Burrito you made rate_limit={rate_limit} and time_limit={time_limit}? "
                "BOTH MUST BE ABOVE ZERO. THANK YOU. BYE."
            )
        self.rate_limit = rate_limit
        self.time_limit = time_limit
        self.timeout = timeout if timeout >= 0 else time_limit
        self.redis = redis
        self.prefix = prefix
        self.message = message
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        logger.debug("Checking throttle data only for Messages and Callback queries")
        if isinstance(event, Message | CallbackQuery):
            key = f"{self.prefix}_{event.from_user.id}"
            throttle = self.redis.get(key) or 0

            logger.debug("Checking interaction rate is lower than rate limit")
            if int(throttle) == self.rate_limit:
                logger.info(f"User: {event.from_user.id} is throttled for {self.time_limit}s")
                pipe = self.redis.pipeline()
                pipe.incr(key).expire(key, self.time_limit)
                pipe.execute()
                username = get_username_or_name(event)
                await event.bot.send_message(event.chat.id, self.message.format(username))
                if not isinstance(event, CallbackQuery):
                    await try_delete_message(event)
            elif int(throttle) > self.rate_limit:
                logger.debug(f"User: {event.from_user.id} is throttled. No response.")
                if not isinstance(event, CallbackQuery):
                    await try_delete_message(event)
            else:
                logger.debug(f"User: {event.from_user.id} is not throttled. Passing response.")
                pipe = self.redis.pipeline()
                pipe.incr(key).expire(key, self.time_limit)
                pipe.execute()
                await handler(event, data)
        else:
            logger.debug("Not Message or CallbackQuery. Passing response.")
            await handler(event, data)

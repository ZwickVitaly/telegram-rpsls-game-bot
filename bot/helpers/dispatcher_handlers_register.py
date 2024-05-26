from aiogram import Dispatcher
from typing import Any


def message_handlers_register(
        dp: Dispatcher, handlers_list: list[tuple[Any | Any | dict] | list[tuple[Any | dict]]]
) -> None:
    for handler in handlers_list:
        if isinstance(handler[1], dict):
            dp.message.register(handler[0], **handler[1])
        else:
            dp.message.register(handler[0], *handler[1], **handler[2])


def callback_handlers_register(
        dp: Dispatcher, handlers_list: list[tuple[Any | Any | dict] | list[tuple[Any | dict]]]
) -> None:
    for handler in handlers_list:
        if isinstance(handler[1], dict):
            dp.message.register(handler[0], **handler[1])
        else:
            dp.message.register(handler[0], *handler[1], **handler[2])
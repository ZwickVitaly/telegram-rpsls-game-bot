import asyncio

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from helpers import is_group, try_delete_message
from keyboards import rpsls_kb
from messages import (
    ONLY_GROUP_REPLY_MESSAGE,
    RANDOM_RPSLS_NEW_GAME_MESSAGE,
    RPSLS_GAME_INVITE_EXPIRED,
    RPSLS_GAME_STARTED_MESSAGE,
    RPSLS_NO_CHOICE_MESSAGE,
    RPSLS_SECOND_PLAYER_FOUND,
    YOU_ARE_ALREADY_IN_GAME_MESSAGE,
)
from settings import (
    RPSLS_GAME_INDEX_KEY,
    RPSLS_GAME_ROUND_TIMER,
    RPSLS_GAME_START_TIMER,
    RPSLS_START_COMMAND,
    logger,
)
from utils import redis_connection


async def start_rpsls_command_handler(message: Message):
    logger.info(f"User: {message.from_user.id} used {RPSLS_START_COMMAND} command")
    delete_message = asyncio.create_task(try_delete_message(message))
    # TODO Мидлварь на проверку группы
    if not is_group(message):
        logger.info(f"User: {message.from_user.id} denied. Not a group chat.")
        await message.answer(ONLY_GROUP_REPLY_MESSAGE)
        return

    logger.debug(f"Chat: {message.chat.id} is group chat")
    user_id = message.from_user.id

    answer_callback = None

    if message.from_user.username:
        username = f"@{message.from_user.username}"
    else:
        username = message.from_user.first_name

    game_index_name = f"{message.chat.id}_{RPSLS_GAME_INDEX_KEY}"
    logger.debug(f"Getting latest game index by name: {game_index_name}")
    game_index = redis_connection.get(game_index_name)

    logger.debug(f"Getting latest game name by index: {game_index}")
    game_name = f"{message.chat.id}_rpsls_game:{game_index}"

    logger.debug(f"Getting latest game data by game_name: {game_name}")
    latest_game = redis_connection.hgetall(game_name)

    if not latest_game or latest_game.get("player_2"):
        logger.debug(f"Game: {game_name} does not exist or full")
        logger.debug(f"Incrementing game index")

        game_index = redis_connection.incr(game_index_name)
        game_name = f"{message.chat.id}_rpsls_game:{game_index}"
        logger.debug(f"New game name: {game_name}")

        logger.debug("Setting new game data and player_1 data")
        pipe = redis_connection.pipeline()
        (
            pipe.hset(game_name, mapping={"player_1": user_id})
            .expire(game_name, RPSLS_GAME_START_TIMER)
            .set(
                f"{message.chat.id}_{user_id}_rpsls_game_name",
                game_name,
                ex=RPSLS_GAME_START_TIMER,
            )
            .set(f"{user_id}_username", username)
        )
        pipe.execute()
        await message.answer(RANDOM_RPSLS_NEW_GAME_MESSAGE.format(username))

        logger.debug(f"Sleeping for {RPSLS_GAME_START_TIMER - 1} seconds")
        await asyncio.sleep(RPSLS_GAME_START_TIMER - 1)

        logger.debug(f"Checking if game: {game_name} still exists after invite.")
        game_exists = redis_connection.hgetall(game_name)
        if game_exists:
            logger.debug(f"Game: {game_name} exists after invite.")
            if game_exists.get("player_2"):
                logger.debug(
                    f"Game: {game_name} there is a second player after invite. Passing"
                )
            else:
                redis_connection.delete(game_name)
                await message.answer(RPSLS_GAME_INVITE_EXPIRED.format(username))
                if answer_callback:
                    await answer_callback.delete()
                logger.debug(
                    f"Game: {game_name} no second player after invite. Expired."
                )
        else:
            logger.debug(f"Game: {game_name} does not exist after invite. All ok.")
    else:
        logger.debug(f"Game: {latest_game}")
        logger.debug(f"Player_2 not found")
        player_1 = redis_connection.hget(game_name, "player_1")
        logger.debug(f"Player_1: {player_1}, User: {user_id}")

        if user_id == int(player_1):
            logger.debug(f"User: {user_id} is already in game")
            await message.answer(YOU_ARE_ALREADY_IN_GAME_MESSAGE)

        else:
            logger.debug("Getting player_1 id")
            player_1_id = redis_connection.hget(game_name, "player_1")

            logger.debug(f"Getting player_1 username by id: {player_1_id}")
            player_1_username = redis_connection.get(f"{player_1_id}_username")

            logger.debug("Setting player_2 data, game data and player_1 game data")
            pipe = redis_connection.pipeline()
            (
                pipe.hset(game_name, mapping={"player_2": user_id})
                .set(f"{user_id}_username", username)
                .set(
                    f"{message.chat.id}_{user_id}_rpsls_game_name",
                    game_name,
                    ex=RPSLS_GAME_ROUND_TIMER,
                )
                .set(
                    f"{message.chat.id}_{player_1}_rpsls_game_name",
                    game_name,
                    ex=RPSLS_GAME_ROUND_TIMER,
                )
            )
            pipe.execute()

            await message.answer(RPSLS_SECOND_PLAYER_FOUND.format(username))
            answer_callback = await message.answer(
                RPSLS_GAME_STARTED_MESSAGE.format(
                    user_1=player_1_username, user_2=username
                ),
                reply_markup=rpsls_kb(),
            )

            logger.debug(f"Sleeping for {RPSLS_GAME_ROUND_TIMER - 1} sec")
            await asyncio.sleep(RPSLS_GAME_ROUND_TIMER - 1)

            logger.debug(
                f"Checking if game: {game_name} still exists after second player join."
            )
            game_exists = redis_connection.exists(game_name)
            if game_exists:
                logger.debug(f"Game: {game_name} exists after second player join.")
                player_1_choice = ...
            else:
                logger.debug(f"Game: {game_name} does not exist after invite. All ok.")
    await delete_message

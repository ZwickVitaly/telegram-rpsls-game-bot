from time import time

from aiogram.types import BufferedInputFile, CallbackQuery
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from db import RPSLSStats, async_session
from games.rpsls import (  # Needed for evaluating by eval()
    Lizard,
    Paper,
    Rock,
    Scissors,
    Spock,
)
from helpers import eval_gif_path, eval_result_string, get_username_or_name
from messages import (
    CHOICE_MADE_MESSAGE,
    CHOICE_RENEW_MESSAGE,
    OOPS_ERROR_MESSAGE,
    PREVIOUS_CALLBACK_MESSAGE_CLICK,
)
from settings import NGINX_STATIC, RPSLS_START_COMMAND, logger
from utils import redis_connection


async def rpsls_choice_callback_handler(callback_query: CallbackQuery):
    logger.debug("Computing answer to callback data")
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id

    logger.debug(f"User id: {user_id}")
    game_name_key_string = f"{chat_id}_{{user_id}}_rpsls_game_name"
    current_user_game_name_key = game_name_key_string.format(user_id=user_id)
    game_name = redis_connection.get(current_user_game_name_key)
    logger.debug(f"Game name: {game_name}")

    if not game_name:
        logger.debug(f"Game name ({game_name}) not found, answering message.")
        await callback_query.message.answer(
            f"Ты не участвуешь ни в одной игре! Нажми {RPSLS_START_COMMAND}, чтобы поучаствовать."
        )

    else:
        logger.debug(f"Game name found: {game_name}")
        username = get_username_or_name(callback_query)

        logger.debug("Getting game data by game name")
        game = redis_connection.hgetall(game_name)

        if not game:
            logger.debug(f"{game}, game data not found.")
            await callback_query.message.answer(OOPS_ERROR_MESSAGE)

        elif not game.get("player_2"):
            logger.warning(
                "No second player. This should not be possible. User must be clicking previous inline keyboard"
            )
            await callback_query.message.answer(PREVIOUS_CALLBACK_MESSAGE_CLICK)

        else:
            player_choice_string = f"{chat_id}_{{user_id}}_game_choice"
            logger.debug("Getting player choice and it's expire time")
            pipe = redis_connection.pipeline()
            current_player_choice_string = player_choice_string.format(user_id=user_id)
            pipe.get(current_player_choice_string).expiretime(
                current_player_choice_string
            )
            player_choice, player_choice_expires = pipe.execute()

            if player_choice_expires < 0:
                logger.debug(
                    f"{player_choice}: {player_choice_expires} - There was no player choice, setting"
                    f"expiration variable to 30 sec"
                )
                player_choice_expires = 30

            else:
                logger.debug(
                    f"{player_choice}: {player_choice_expires} - There was player choice, setting"
                    f"expiration variable to time left"
                )
                player_choice_expires -= int(time())

            callback_data = callback_query.data
            logger.debug(f"{callback_data}: callback data, setting to redis")
            redis_connection.set(
                current_player_choice_string, callback_data, ex=player_choice_expires
            )

            if player_choice:
                logger.debug(
                    f"{player_choice}: choice is already made. Renew message sent"
                )
                await callback_query.message.answer(
                    CHOICE_RENEW_MESSAGE.format(username)
                )

            else:
                logger.debug(f"{player_choice}: no previous choice")
                await callback_query.message.answer(
                    CHOICE_MADE_MESSAGE.format(username)
                )

                logger.debug(
                    f"Getting player ids from game info to check if there are two player choices"
                )
                player_1_id = game.get("player_1")
                player_2_id = game.get("player_2")

                logger.debug(
                    f"Player_1_id={player_1_id}, Player_2_id={player_2_id}, Chat: {chat_id} getting choices"
                )
                pipe = redis_connection.pipeline()
                (
                    pipe.get(player_choice_string.format(user_id=player_1_id)).get(
                        player_choice_string.format(user_id=player_2_id)
                    )
                )
                player_1_choice, player_2_choice = pipe.execute()

                if player_1_choice and player_2_choice:
                    logger.debug(
                        f"Both players made choice. Player_1={player_1_choice}, Player_2={player_2_choice}"
                        f"Deleting game info by game name ({game_name}) from redis"
                    )
                    redis_connection.delete(game_name)

                    pipe = redis_connection.pipeline()
                    (pipe.get(f"{player_1_id}_username").get(f"{player_2_id}_username"))
                    player_1_username, player_2_username = pipe.execute()
                    logger.debug(
                        f"Getting players usernames: Player_1: {player_1_username}, Player_2: {player_2_username}"
                    )
                    logger.debug(f"Sending 'game pending' messages")
                    await callback_query.message.answer("Сравниваем...")
                    await callback_query.message.answer("Анализируем...")
                    await callback_query.message.answer("Вычисляем...")

                    logger.debug("Evaluating player chocies as python classes")
                    player_1_choice = eval(
                        player_1_choice.format(player_1_id, player_1_username)
                    )
                    player_2_choice = eval(
                        player_2_choice.format(player_2_id, player_2_username)
                    )

                    logger.debug("Evaluating winner through '==' comparison ")
                    win_fig, loose_fig = player_1_choice == player_2_choice

                    logger.debug(
                        f"win_fig={win_fig}, loose_fig={loose_fig}. Evaluating result_message"
                    )
                    result_message = eval_result_string(win_fig, loose_fig)
                    logger.info(result_message)

                    logger.debug(f"Evaluating result gif path.")
                    result_gif_path = eval_gif_path(win_fig, loose_fig)
                    if NGINX_STATIC:
                        await callback_query.message.bot.send_animation(
                            chat_id, result_gif_path
                        )
                    else:
                        try:
                            logger.debug(f"Trying to open {result_gif_path}")
                            with open(result_gif_path, "rb") as file:
                                gif = BufferedInputFile(
                                    file.read(), filename="result.gif"
                                )
                            await callback_query.message.bot.send_animation(
                                chat_id, gif
                            )
                            logger.debug("Success")
                        except IOError:
                            logger.error(
                                f"File {result_gif_path} does not exist. Perhaps you forgot to put gifs in static?"
                            )

                    logger.debug(f"Sending result message: {result_message.strip()}")
                    await callback_query.message.answer(result_message)

                    logger.debug("Deleting players choices and game name")
                    pipe = redis_connection.pipeline()
                    (
                        pipe.delete(player_choice_string.format(user_id=player_1_id))
                        .delete(player_choice_string.format(user_id=player_2_id))
                        .delete(game_name_key_string.format(user_id=player_1_id))
                        .delete(game_name_key_string.format(user_id=player_2_id))
                    )
                    pipe.execute()
                    await callback_query.message.delete()
                    if win_fig:
                        logger.debug("Trying to update win-loose stats")
                        async with async_session() as session:
                            async with session.begin():
                                try:
                                    await session.execute(
                                        update(RPSLSStats)
                                        .where(user_id == int(win_fig.user_id))
                                        .values(wins=RPSLSStats.wins + 1)
                                    )
                                    await session.execute(
                                        update(RPSLSStats)
                                        .where(user_id == int(loose_fig.user_id))
                                        .values(wins=RPSLSStats.losses + 1)
                                    )
                                    logger.debug(
                                        f"Stats are updated for players: {win_fig.user_id}, {loose_fig.user_id}"
                                    )
                                except IntegrityError as e:
                                    logger.error(
                                        f"Something wrong with updating RPSLStats: {e}"
                                    )
                    else:
                        logger.info(
                            f"{player_1_username}({player_1_id}) - {player_2_username}({player_2_id}) "
                            f"| Tie, stats are not updated"
                        )

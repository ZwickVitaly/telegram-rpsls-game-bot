from settings import (
    REGISTER_COMMAND,
    RPSLS_GAME_ROUND_TIMER,
    RPSLS_GAME_START_TIMER,
    RPSLS_START_COMMAND,
)

# Basic /start command message
RPSLS_START_COMMAND_MESSAGE = f"""КАМЕНЬ-НОЖНИЦЫ-БУМАГА-ЯЩЕРИЦА-СПОК.\n
    Чтобы сыграть выбери команду:\n
    {REGISTER_COMMAND} - зарегистрироваться для ведения статистики (необязательно)\n
    {RPSLS_START_COMMAND} - начать предложить игру. Первый, кто согласится - играет с тобой.
    Принять приглашение можно этой-же командой.\n"""
#     "/rpsls_rumble - начать игру-потасовку. 60 секунд ждём игроков, если набирается "
#     "меньше 5, отменяем. Если набирается 10 - начинаем. Каждый выбирает свой знак,"
#     "Сравниваем в случайном порядке. 1 победитель.\n"
#     "/rpsls_tournament - турнир. Минимум 4 участника, максимум 20. Соперники подбираются случайно"
#     "Выбор на каждый \"бой\". Перевыбор если ничья. Те, кто без пары - ждут."
#     "1 победитель."

RANDOM_RPSLS_NEW_GAME_MESSAGE = f"""{{}} предлагает сыграть в КНБЯС. 
Поддержите бедолагу: {RPSLS_START_COMMAND} 
Через {RPSLS_GAME_START_TIMER} секунд приглашение протухнет."""

HAVE_WON_MESSAGE = "Победил(а)"
BOTH_CHOSE_MESSAGE = "Оба выбрали"
TIE_MESSAGE = "Ничья."

RPSLS_NO_CHOICE_MESSAGE = (
    "Щас бы начать игру и не выбирать... А ещё меня ботом обзывают..."
)

YOU_ARE_ALREADY_IN_GAME_MESSAGE = "Падажжи, ты уже играешь."

RPSLS_GAME_STARTED_MESSAGE = (
    f"{{user_1}} и {{user_2}} в зарубе. У вас {RPSLS_GAME_ROUND_TIMER} секунд."
)

RPSLS_SECOND_PLAYER_FOUND = "Опа а вот и второй КНБЯСник. {}"

RPSLS_GAME_INVITE_EXPIRED = "Вот так тут поддерживают, {} Приглашение протухло "

RPSLS_GAME_INVITE_CALLBACK_EXPIRED = "Приглашение"

NEW_PLAYER_REGISTER_MESSAGE = "Ещё и за тобой записывать, {}"

CHOICE_MADE_MESSAGE = "{} выбор сделан"
CHOICE_RENEW_MESSAGE = "{} выбор обновлён"

PREVIOUS_CALLBACK_MESSAGE_CLICK = "Ну куда ты жмакаешь? Там уже всё похерено, прекрати."


LOOKING_FOR_STATS_MESAGE = "Да дааа, сейчас гляну"

STATS_FOUND_MESSAGE = "{username}:\nПовезло: {wins} {times_w}\nПотрачено: {losses} {times_l}"
STATS_NOT_FOUND_MESSAGE = f"{{username}} ты издеваешься? Зарегайся сначала {REGISTER_COMMAND}, потом стату проси"
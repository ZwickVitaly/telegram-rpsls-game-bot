from settings import logger


class _Figure:
    accusative = None
    emoji = None

    def __init__(self, user_id: int, username: str):
        logger.debug(f"{user_id} - {username} chose {self.__class__.__name__}")
        self.user_id = user_id
        self.username = username

    @classmethod
    def string_callback(cls):
        return f"{cls.__name__}('{{}}', '{{}}')"

    @classmethod
    def class_name_lower(cls):
        return cls.__name__.lower()


class Rock(_Figure):
    accusative = "камень"
    emoji = "🪨"

    def __eq__(self, other: _Figure):
        logger.debug(f"{self.__class__.__name__} == {other.__class__.__name__}")
        if isinstance(other, Scissors | Lizard | None):
            logger.debug(f"{self.__class__} winner, {other.__class__.__name__} looser")
            return self, other
        elif isinstance(other, Paper | Spock):
            logger.debug(f"{self.__class__} looser, {other.__class__.__name__} winner")
            return other, self
        logger.debug("Tie")
        return None, self

    def __str__(self):
        return "Камень"


class Paper(_Figure):
    accusative = "бумагу"
    emoji = "📜"

    def __eq__(self, other):
        logger.debug(f"{self.__class__.__name__} == {other.__class__.__name__}")
        if isinstance(other, Rock | Spock | None):
            logger.debug(f"{self.__class__} winner, {other.__class__.__name__} looser")
            return self, other
        elif isinstance(other, Scissors | Lizard):
            logger.debug(f"{self.__class__} looser, {other.__class__.__name__} winner")
            return other, self
        logger.debug("Tie")
        return None, self

    def __str__(self):
        return "Бумага"


class Scissors(_Figure):
    accusative = "ножницы"
    emoji = "✂️"

    def __eq__(self, other):
        logger.debug(f"{self.__class__.__name__} == {other.__class__.__name__}")
        if isinstance(other, Paper | Lizard | None):
            logger.debug(f"{self.__class__} winner, {other.__class__.__name__} looser")
            return self, other
        elif isinstance(other, Rock | Spock):
            logger.debug(f"{self.__class__} looser, {other.__class__.__name__} winner")
            return other, self
        logger.debug("Tie")
        return None, self

    def __str__(self):
        return "Ножницы"


class Lizard(_Figure):
    accusative = "ящерицу"
    emoji = "🦎"

    def __eq__(self, other):
        logger.debug(f"{self.__class__.__name__} == {other.__class__.__name__}")
        if isinstance(other, Paper | Spock | None):
            logger.debug(f"{self.__class__} winner, {other.__class__.__name__} looser")
            return self, other
        elif isinstance(other, Rock | Scissors):
            logger.debug(f"{self.__class__} looser, {other.__class__.__name__} winner")
            return other, self
        logger.debug("Tie")
        return None, self

    def __str__(self):
        return "Ящерица"


class Spock(_Figure):
    accusative = "Спока"
    emoji = "🖖"

    def __eq__(self, other):
        logger.debug(f"{self.__class__.__name__} == {other.__class__.__name__}")
        if isinstance(other, Scissors | Rock | None):
            logger.debug(f"{self.__class__} winner, {other.__class__.__name__} looser")
            return self, other
        elif isinstance(other, Lizard | Paper):
            logger.debug(f"{self.__class__} looser, {other.__class__.__name__} winner")
            return other, self
        logger.debug("Tie")
        return None, self

    def __str__(self):
        return "Спок"


RPC_FILTER_LIST = [
    Rock.string_callback(),
    Paper.string_callback(),
    Scissors.string_callback(),
    Lizard.string_callback(),
    Spock.string_callback(),
]
logger.debug(f"Formed figures string callbacks: {' | '.join(RPC_FILTER_LIST)}")

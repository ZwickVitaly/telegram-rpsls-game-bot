from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from games.rpsls import Rock, Paper, Scissors, Spock, Lizard


def rpsls_kb() -> InlineKeyboardMarkup:
    rock = InlineKeyboardButton(text=Rock.emoji, callback_data=Rock.string_callback())
    scissors = InlineKeyboardButton(text=Scissors.emoji, callback_data=Scissors.string_callback())
    paper = InlineKeyboardButton(text=Paper.emoji, callback_data=Paper.string_callback())
    lizard = InlineKeyboardButton(text=Lizard.emoji, callback_data=Lizard.string_callback())
    spock = InlineKeyboardButton(text=Spock.emoji, callback_data=Spock.string_callback())
    rows = [
        [rock],
        [scissors],
        [paper],
        [lizard],
        [spock],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)

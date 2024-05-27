from .check_is_group import is_group
from .delete_message_from_chat import try_delete_message
from .get_username_or_first_name import get_username_or_name
from .rpsls_funcs import eval_gif_path, eval_result_string
from ru_plural import times_plural

__all__ = [
    "eval_result_string",
    "eval_gif_path",
    "is_group",
    "get_username_or_name",
    "try_delete_message",
    "times_plural"
]

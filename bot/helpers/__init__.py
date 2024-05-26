from .rpsls_funcs import eval_gif_path, eval_result_string
from .check_is_group import is_group
from .get_username_or_first_name import get_username_or_name
from .delete_message_from_chat import try_delete_message


__all__ = [
    "eval_result_string",
    "eval_gif_path",
    "is_group",
    "get_username_or_name",
    "try_delete_message",
]

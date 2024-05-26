from messages import HAVE_WON_MESSAGE, BOTH_CHOSE_MESSAGE, TIE_MESSAGE
from settings import STATIC_PATH


def eval_gif_path(win_fig, loose_fig) -> str:
    if win_fig:
        gif_path = (f"{STATIC_PATH}{win_fig.class_name_lower()}/"
                    f"{win_fig.class_name_lower()}-{loose_fig.class_name_lower()}.gif")
        return gif_path
    gif_path = (f"{STATIC_PATH}{loose_fig.__class__.__name__.lower()}/"
                f"{loose_fig.class_name_lower()}-{loose_fig.class_name_lower()}.gif")
    return gif_path


def eval_result_string(win_fig, loose_fig) -> str:
    if win_fig:
        return (f"{win_fig.username}: {win_fig}\n{loose_fig.username}: {loose_fig}\n"
                f"{HAVE_WON_MESSAGE} {win_fig.username}")
    else:
        return f"{BOTH_CHOSE_MESSAGE} {loose_fig.accusative}. {TIE_MESSAGE}"

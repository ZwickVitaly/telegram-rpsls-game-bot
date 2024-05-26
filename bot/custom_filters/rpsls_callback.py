from games.rpsls import RPC_FILTER_LIST
from settings import logger


def rpsls_callback_filter(cb):
    logger.debug("Filtering callback")
    try:
        if any([figure == cb.data for figure in RPC_FILTER_LIST]):
            logger.debug(f"Callback {cb.data} in {RPC_FILTER_LIST}")
            return True
        logger.debug(f"Callback {cb.data} not in {RPC_FILTER_LIST}")
    except AttributeError:
        logger.debug(f"No callback data")
        return

from functools import wraps
import logging
import time


def create_logger(logger_name):
    """
    Create logger
    """
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter(
        "\n[%(levelname)s|%(name)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s"
    )

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(log_format)
    logger.addHandler(console)

    return logger


logger = create_logger(__name__)


def log_excution_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        elasped_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {elasped_time:.2f} seconds")
        return result

    return wrapper
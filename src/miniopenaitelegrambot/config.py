import sys
import tracemalloc

from dataclasses import dataclass

import environs
from loguru import logger


env = environs.Env()
env.read_env()

# To get the object allocation traceback when using asynchrony
tracemalloc.start()


@dataclass
class Config:
    try:
        TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN")
        TELEGRAM_USERS = env.list("TELEGRAM_USERS", validate=lambda n: all(user.isdecimal() for user in n))
        OPENAI_API_KEY = env.str("OPENAI_API_KEY")
        DEBUG = env.bool("DEBUG", default=False)
        TRACE_LOG = env.bool("TRACE_LOG", default=False)
    except environs.EnvError as e:
        logger.opt(exception=False).error(e)
        sys.exit(1)


def setup_logging(log, debug=False, trace=False):
    log.remove()

    if debug:
        log.add(
            'logs/debug.log',
            level='DEBUG',
            colorize=True,
            backtrace=True,
            diagnose=True,
            enqueue=True,
            catch=True,
            delay=True,
        )

    if trace:
        log.add(
            'logs/trace.log',
            level='TRACE',
            colorize=False,
            backtrace=False,
            diagnose=False,
            enqueue=True,
            catch=False,
            delay=True,
        )

    log.add(
        sys.stdout,
        level='DEBUG' if debug else 'INFO',
        colorize=True,
        backtrace=debug,
        diagnose=debug,
        enqueue=True,
        catch=True,
    )

    log.add(
        'logs/error.log',
        level='ERROR',
        colorize=True,
        backtrace=True,
        diagnose=debug,
        enqueue=True,
        catch=True,
        rotation='10 MB' if debug else None,
        compression='zip' if debug else None,
        delay=True,
    )

    log.debug(f"Logging handlers configured:\n{log}")

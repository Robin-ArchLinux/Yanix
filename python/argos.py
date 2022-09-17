from xmlrpc.client import Boolean
import sys
from loguru import logger


class Argos:
    def configure(is_debug: Boolean = False):
        if not is_debug:
            config = {
                "handlers": [
                    {"sink": sys.stdout, "format": "<level>{message}</level>"},
                    {"sink": "file.log", "serialize": True},
                ],
                "extra": {"user": "someone"}
            }
            logger.configure(**config)

    def trace(msg):
        logger.opt(depth=1).trace(msg)

    def w(msg):
        logger.opt(depth=1).warning(msg)

    def i(msg):
        logger.opt(depth=1).info(msg)

    def s(msg):
        logger.opt(depth=1).success(msg)

    def d(msg):
        logger.opt(depth=1).debug(msg)

    def e(msg):
        logger.opt(depth=1).error(msg)

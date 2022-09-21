import sys
from xmlrpc.client import Boolean
import os
from loguru import logger


class Argos:
    @staticmethod
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

    @staticmethod
    def trace(msg):
        logger.opt(depth=1).trace(msg)

    @staticmethod
    def w(msg):
        logger.opt(depth=1).warning(msg)

    @staticmethod
    def i(msg):
        logger.opt(depth=1).info(msg)

    @staticmethod
    def s(msg):
        logger.opt(depth=1).success(msg)

    @staticmethod
    def d(msg):
        logger.opt(depth=1).debug(msg)

    @staticmethod
    def e(msg):
        logger.opt(depth=1).error(msg)
        sys.exit(1)

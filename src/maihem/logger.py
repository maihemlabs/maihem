import os
from loguru import logger
import sys


class Logger:
    def __init__(self, name: str, level="DEBUG"):
        self.name = name

        # Remove default handler
        logger.remove()

        # Add custom handler
        logger.add(
            sys.stdout,
            colorize=True,
            format=self.format_message,
            level=level,
            filter=self.add_extra_fields,
        )

    def format_message(self, record):
        base_format = "<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> - <level>{level}</level> - {message}"
        if record["extra"]["request_id"]:
            base_format += " - <dim>request_id:{extra[request_id]}</dim>"
        base_format += "\n"
        return base_format

    def add_extra_fields(self, record):
        record["extra"]["request_id"] = ""
        return True

    def debug(self, msg: str, *args, **kwargs):
        logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        logger.exception(msg, *args, **kwargs)


logger_instance = Logger(name="maihem-python-sdk")


def get_logger():
    return logger_instance

import sys, os
from loguru import logger
from typing import TYPE_CHECKING
from .request_context import (
    get_request_id,
    get_test_run_id,
    get_conversation_id,
    get_workflow_span_id,
    get_workflow_trace_id,
    get_workflow_trace_raw_id,
    get_workflow_step_id,
)

if TYPE_CHECKING:
    from loguru import Logger

from loguru._logger import Logger

extra_fields = [
    "request_id",
    "test_run_id",
    "conversation_id",
    "workflow_trace_id",
    "workflow_trace_raw_id",
    "workflow_span_id",
    "workflow_step_id",
]


def _add_extra_fields(record):
    record["extra"]["request_id"] = get_request_id()
    record["extra"]["test_run_id"] = get_test_run_id()
    record["extra"]["conversation_id"] = get_conversation_id()
    record["extra"]["workflow_trace_id"] = get_workflow_trace_id()
    record["extra"]["workflow_trace_raw_id"] = get_workflow_trace_raw_id()
    record["extra"]["workflow_span_id"] = get_workflow_span_id()
    record["extra"]["workflow_step_id"] = get_workflow_step_id()
    return True


def add_default_logger(logger: Logger, level: str = "DEBUG"):
    logger.remove()

    def format_message(record):
        # Add a relative pathname to 'extra', but do not overwrite existing keys
        record["extra"][
            "pathname"
        ] = f"{os.path.relpath(record['file'].path)}:{record['line']}"

        # Base format string
        base_format = (
            "<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> - "
            "<level>{level}</level> - {message} - "
            "<dim>{extra[pathname]}</dim>"
        )

        # Add any additional 'extra' fields dynamically
        for key, value in record["extra"].items():
            if key == "pathname":  # Skip 'pathname' since it's already included
                continue
            if value:  # Only include non-empty values
                base_format += f" - <dim>{key}:{{extra[{key}]}}</dim>"

        # Include exception details if present
        if record["exception"]:
            base_format += "\n<red>{exception}</red>"

        base_format += "\n"
        return base_format

    logger.add(
        sys.stdout,
        colorize=True,
        format=format_message,
        level=level,
        filter=_add_extra_fields,
        backtrace=True,
        diagnose=False,
    )


def get_logger() -> Logger:
    return logger

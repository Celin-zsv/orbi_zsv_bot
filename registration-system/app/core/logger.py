from functools import partial
from json import dumps
from os import getpid

import structlog
from structlog.contextvars import merge_contextvars
from structlog.processors import JSONRenderer, TimeStamper, UnicodeDecoder, add_log_level

from app.core.config import settings

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def add_pid(logger, log_method, event_dict):
    event_dict["pid"] = getpid()
    return event_dict


structlog.configure(
    processors=[
        merge_contextvars,
        add_pid,
        add_log_level,
        TimeStamper(fmt=DATETIME_FORMAT, utc=False),
        UnicodeDecoder(),
        JSONRenderer(serializer=partial(dumps, ensure_ascii=False)),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(settings.log_level),
)

log = structlog.get_logger()

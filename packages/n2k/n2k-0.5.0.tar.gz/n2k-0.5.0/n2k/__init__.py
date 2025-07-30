import logging

from . import messages, types, utils
from .can_message import N2kCANMessage
from .device import Device
from .device_information import DeviceInformation
from .device_list import DeviceList

# from .group_function import ?
# from .group_function_default_handlers import ?
from .message import Message
from .message_handler import MessageHandler
from .n2k import PGN
from .node import Node

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

__all__ = [
    "PGN",
    "Device",
    "DeviceInformation",
    "DeviceList",
    "Message",
    "MessageHandler",
    "N2kCANMessage",
    "Node",
    "messages",
    "set_log_level",
    "types",
    "utils",
]


def set_log_level(level: int) -> None:
    if level > logging.DEBUG >= log.level:
        log.setLevel(level)
        log.removeHandler(debug_console_handler)
        log.addHandler(console_handler)
    elif level <= logging.DEBUG < log.level:
        log.setLevel(level)
        log.removeHandler(console_handler)
        log.addHandler(debug_console_handler)
    else:
        log.setLevel(level)


debug_console_handler = logging.StreamHandler()
debug_console_handler.setFormatter(
    logging.Formatter(
        "[{asctime:s}] - {levelname:<8s} - {name:s} - {filename:s}:{lineno:d}->{funcName:s}\n"
        + "" * (23 + 3)
        + "{message:s}",
        style="{",
    ),
)


console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter(
        "[{asctime:s}] - {levelname:<8s} - {name:s} - {message:s}",
        style="{",
    ),
)
log.addHandler(console_handler)

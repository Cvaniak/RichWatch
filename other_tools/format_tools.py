from datetime import datetime
from typing import Dict, Tuple
from config import type_dict, style_dict, OTHER_TYPE
from rich.text import Text


def format_date(date: datetime.timestamp) -> str:
    d = datetime.fromtimestamp(date / 1000.0)
    time = d.strftime("%m/%d/%Y\n%H:%M:%S.%f")[:-3]
    return time


def format_message(message: str) -> Tuple[str, str]:
    if not message:
        return OTHER_TYPE, message

    message_type = [x for x in type_dict.keys() if message.startswith(x)]

    if message_type:
        type_length = len(message_type[0])
        message_body = message[type_length:]
        message_type = type_dict[message_type[0]]
    else:
        message_type = OTHER_TYPE
        message_body = message

    tmp = message_body.replace("\t", "\n")
    tmp = tmp.strip()
    message_body = tmp

    return message_type, message_body


def format_event(event: Dict) -> Tuple[str, Text, str]:
    date = format_date(event["timestamp"])
    message_type, message_body = format_message(event["message"])

    return (
        date,
        Text(message_type.upper(), style=style_dict[message_type]),
        message_body,
    )

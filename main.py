from datetime import datetime

import boto3
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text

type_dict = {
    "[INFO]": "info",
    "[WARNING]": "warning",
    "[ERROR]": "error",
    "START": "start",
    "REPORT": "report",
    "END": "end",
    "DEBUG": "debug",
}

style_dict = {
    "error": "bold red",
    "start": "green",
    "report": "dim yellow",
    "debug": "bold blue",
    "warning": "yellow",
    "info": "yellow",
    "end": "cyan",
}

OTHER_TYPE = "debug"


def format_date(date):
    d = datetime.fromtimestamp(date / 1000.0)
    time = d.strftime("%m/%d/%Y\n%H:%M:%S.%f")[:-3]
    return time


def format_message(message):
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


def format_event(event):
    date = format_date(event["timestamp"])
    message_type, message_body = format_message(event["message"])

    return (
        date,
        Text(message_type.upper(), style=style_dict[message_type]),
        message_body,
    )


def create_log_table(client, log_name):
    stream_response = client.describe_log_streams(
        logGroupName=log_name,
        orderBy="LastEventTime",
        descending=True,
        limit=2,
    )

    list_log_streams = stream_response["logStreams"]

    table = Table(title=log_name, box=box.MINIMAL,
                  show_lines=True, highlight=None)
    table.add_column("Time")
    table.add_column("Type")
    table.add_column("Massage")
    for log_detail in list_log_streams:
        response = client.get_log_events(
            logGroupName=log_name,
            logStreamName=log_detail["logStreamName"],
        )

        for event in response["events"]:
            table.add_row(*format_event(event))

    return table


if __name__ == "__main__":

    client = boto3.client("logs")
    log_name = "/aws/lambda/data-upload-lambda-receive-sqs-infra"

    console = Console()
    console.print(create_log_table(client, log_name))

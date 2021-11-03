from rich import box
from other_tools.format_tools import format_event
from rich.table import Table
from boto3 import client
import sys


def create_log_table(client: client, log_name: str):
    stream_response = client.describe_log_streams(
        logGroupName=log_name,
        orderBy="LastEventTime",
        descending=True,
        limit=2,
    )

    list_log_streams = stream_response["logStreams"]

    title = log_name.upper().split("/")[-1]
    table = Table(title=title, box=box.MINIMAL,
                  show_lines=True, highlight=None, title_style="bold")
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

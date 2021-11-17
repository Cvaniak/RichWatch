from typing import Dict, List, Tuple, Union
from rich import box
from other_tools.format_tools import format_event
from rich.table import Table
import json
import os

STREAM_FILE = "stream_file.json"


def create_directory(log_group_name: str) -> str:
    directory = os.path.abspath(os.getcwd())

    log_groups_dir = os.path.join(directory, "log_groups")
    if not os.path.exists(log_groups_dir):
        os.makedirs(log_groups_dir)

    log_group_dir = os.path.join(log_groups_dir, log_group_name.split("/")[-1])
    if not os.path.exists(log_group_dir):
        os.makedirs(log_group_dir)

    return log_group_dir


def check_for_new_event(
    list_log_streams: List[Dict], stream_file_dir: str
) -> Tuple[bool, Union[int, None]]:

    if not os.path.exists(stream_file_dir):
        return True, None

    max_timestamp = max([x["lastIngestionTime"] for x in list_log_streams])

    with open(stream_file_dir, "r") as f:
        old_stream = json.load(f)

    max_old_timestamp = max([x["lastIngestionTime"] for x in old_stream])

    is_newer = max_timestamp > max_old_timestamp
    return is_newer, max_old_timestamp if is_newer else None


def download_new_log_stream(client, log_group_name):
    stream_response = client.describe_log_streams(
        logGroupName=log_group_name,
        orderBy="LastEventTime",
        descending=True,
        limit=2,
    )
    list_log_streams = stream_response["logStreams"]
    return list_log_streams


def save_stream_to_file(list_log_streams, log_group_dir):
    stream_file_dir = os.path.join(log_group_dir, STREAM_FILE)
    with open(stream_file_dir, "w") as stream_file:
        json.dump(list_log_streams, stream_file, indent=4, sort_keys=True)


def download_log_group(
    client,
    log_group_name: str,
    list_log_streams: List[Dict],
    from_timestamp: int = None,
) -> Dict:

    optional = dict()
    if from_timestamp is not None:
        optional["startTime"] = from_timestamp

    result = dict()
    for log_detail in list_log_streams:
        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_detail["logStreamName"],
            **optional,
        )

        log_group_short_name = log_detail["logStreamName"].split("]")[-1]
        result[log_group_short_name] = response["events"]

    return result


def save_log_group_to_file(list_of_events: Dict, log_group_dir: str) -> None:
    for event_list_name in list_of_events:
        log_stream_dir = os.path.join(log_group_dir, f"{event_list_name}.json")
        with open(log_stream_dir, "w") as log_file:
            json.dump(
                list_of_events[event_list_name], log_file, indent=4, sort_keys=True
            )


def create_table(log_group_name: str) -> Table:
    title = log_group_name.upper().split("/")[-1]
    table = Table(
        title=title,
        box=box.MINIMAL,
        show_lines=True,
        highlight=False,
        title_style="bold",
    )
    table.add_column("Time")
    table.add_column("Type")
    table.add_column("Massage")
    return table


def create_log_table(log_group_name: str, log_group_dir: str) -> Table:
    with open(os.path.join(log_group_dir, STREAM_FILE), "r") as f:
        stream_file = json.load(f)
    table = create_table(log_group_name)
    for data in stream_file:
        log_file_name = f"{data['logStreamName'].split(']')[-1]}.json"
        with open(os.path.join(log_group_dir, log_file_name), "r") as b:
            c = json.load(b)
            for d in reversed(c):
                table.add_row(*format_event(d))
    return table


def get_log_table(
    client, log_group_name: str, has_table: str = None
) -> Union[Table, None]:
    log_group_dir = create_directory(log_group_name)

    list_log_streams = download_new_log_stream(client, log_group_name)
    needs_update, max_old_timestamp = check_for_new_event(
        list_log_streams, os.path.join(log_group_dir, STREAM_FILE)
    )

    if not needs_update:
        if has_table:
            return None
        create_log_table(log_group_name, log_group_dir)

    save_stream_to_file(list_log_streams, log_group_dir)
    list_of_events = download_log_group(
        client, log_group_name, list_log_streams, max_old_timestamp
    )
    save_log_group_to_file(list_of_events, log_group_dir)

    table = create_log_table(log_group_name, log_group_dir)
    return table

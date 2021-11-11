from other_tools.other import (
    save_log_group_to_file,
    check_for_new_event,
    download_new_log_stream,
    download_log_group,
    create_directory,
    get_log_table,
    save_stream_to_file,
)
import json
from stubber import (
    generate_stubber_logs,
    generate_stubber_logs_with_existing_stream,
    generate_stubber_logs_all_files_in_directory,
)
from rich.table import Table
import os

LOG_GROUP_NAME = "/aws/lambda/test-log-group-definitely-unique"


def clean_up():
    directory = os.path.abspath(os.getcwd())
    log_group = LOG_GROUP_NAME.split("/")[-1]
    log_group_dir = os.path.join(directory, f"log_groups/{log_group}")
    if os.path.exists(log_group_dir):
        arr = os.listdir(log_group_dir)
        for file in arr:
            os.remove(os.path.join(log_group_dir, file))
        os.rmdir(log_group_dir)


def setup_directory(client, log_group_name):
    log_group_dir = create_directory(log_group_name)
    list_log_streams = download_new_log_stream(client, log_group_name)
    save_stream_to_file(list_log_streams, log_group_dir)
    return log_group_dir, list_log_streams


class CleanUpManager:
    def __init__(self):
        ...

    def __enter__(self):
        clean_up()
        return self

    def __exit__(self, *args, **kwargs):
        clean_up()


def test_create_directory():
    with CleanUpManager():
        log_group = LOG_GROUP_NAME.split("/")[-1]
        directory = os.path.abspath(os.getcwd())
        log_group_dir = os.path.join(directory, f"log_groups/{log_group}")
        if os.path.exists(log_group_dir):
            os.rmdir(log_group_dir)
        create_directory(log_group)
        assert os.path.exists(log_group_dir)


def test_check_for_new_event():
    with CleanUpManager():
        directory = os.path.abspath(os.getcwd())
        data_dir = os.path.join(directory, "tests/data/")
        log_group_stream = os.path.join(data_dir, "list_response/stream_file_now.json")

        with open(log_group_stream) as f:
            same_data = json.load(f)
        assert check_for_new_event(same_data, log_group_stream) == (False, None)

        new_log_group_stream = os.path.join(
            data_dir, "list_response/stream_file_older.json"
        )
        with open(new_log_group_stream) as f:
            new_data = json.load(f)
        assert check_for_new_event(new_data, log_group_stream) == (False, None)

        old_log_group_stream = os.path.join(
            data_dir, "list_response/stream_file_newer.json"
        )
        with open(old_log_group_stream) as f:
            old_data = json.load(f)
        assert check_for_new_event(old_data, log_group_stream) == (True, 1636057322368)


def test_downloaded_log_stream():
    directory = os.path.abspath(os.getcwd())
    data_dir = os.path.join(directory, "tests/data/")
    log_group_stream = os.path.join(data_dir, "list_response/stream_file_now.json")

    log_group_name = LOG_GROUP_NAME
    client, stubber = generate_stubber_logs(log_group_name)

    with open(log_group_stream) as file:
        response = json.load(file)

    with stubber:
        downloaded = download_new_log_stream(client, log_group_name)
        for index in range(len(response)):
            for key in downloaded[index]:
                assert downloaded[index][key] == response[index][key]

        downloaded = download_log_group(client, log_group_name, downloaded, None)
        # TODO: is dirty
        assert all(x in ["uniquecode1234", "uniquecode5678"] for x in downloaded.keys())


def test_downloaded_log_group_no_stream_file():
    log_group_name = LOG_GROUP_NAME
    client, stubber = generate_stubber_logs(log_group_name)

    with CleanUpManager():
        with stubber:
            assert isinstance(get_log_table(client, log_group_name), Table)


def test_downloaded_log_group_older_stream_file():
    log_group_name = LOG_GROUP_NAME
    client, stubber = generate_stubber_logs_with_existing_stream(
        log_group_name, "http_response/stream_file_older.json", 1636057312368
    )

    with CleanUpManager():
        with stubber:
            setup_directory(client, log_group_name)
            assert isinstance(get_log_table(client, log_group_name), Table)


def test_downloaded_log_group_same_stream_file_never_drown():
    log_group_name = LOG_GROUP_NAME
    client, stubber = generate_stubber_logs_all_files_in_directory(
        log_group_name, "http_response/stream_file.json"
    )

    with CleanUpManager():
        with stubber:
            log_group_dir, list_log_streams = setup_directory(client, log_group_name)

            list_of_events = download_log_group(
                client, log_group_name, list_log_streams, None
            )
            save_log_group_to_file(list_of_events, log_group_dir)

            assert isinstance(get_log_table(client, log_group_name), Table)


def test_downloaded_log_group_same_stream_file_already_drown():
    log_group_name = LOG_GROUP_NAME
    client, stubber = generate_stubber_logs_with_existing_stream(
        log_group_name, "http_response/stream_file.json"
    )

    with CleanUpManager():
        with stubber:
            setup_directory(client, log_group_name)
            assert get_log_table(client, log_group_name, has_table=True) is None


# Should not happen
def test_downloaded_log_group_newer_stream_file():
    log_group_name = LOG_GROUP_NAME
    client, stubber = generate_stubber_logs_with_existing_stream(
        log_group_name, "http_response/stream_file_newer.json"
    )

    with CleanUpManager():
        with stubber:
            setup_directory(client, log_group_name)
            assert get_log_table(client, log_group_name, has_table=True) is None

import os
import json
import botocore
from botocore.stub import Stubber


def stubber_client_directory():
    client = botocore.session.get_session().create_client("logs")
    directory = os.path.abspath(os.getcwd())

    stubber = Stubber(client)
    return stubber, client, directory


def add_get_log_events(
    stubber, log_group_name, log_stream_name, directory, optional=None
):
    expected_params = {
        "logGroupName": log_group_name,
        "logStreamName": f"2021/11/04/[$LATEST]{log_stream_name}",
    }
    if optional is not None:
        expected_params["startTime"] = optional
    with open(os.path.join(directory, f"tests/data/logs/{log_stream_name}.json")) as f:
        response = json.load(f)
    stubber.add_response("get_log_events", response, expected_params)


def add_describe_log_streams(stubber, log_group_name, log_stream_name, directory):
    expected_params = {
        "logGroupName": log_group_name,
        "orderBy": "LastEventTime",
        "descending": True,
        "limit": 2,
    }

    with open(os.path.join(directory, f"tests/data/{log_stream_name}")) as f:
        response = json.load(f)
    stubber.add_response("describe_log_streams", response, expected_params)


def generate_stubber_logs(log_group_name):
    stubber, client, directory = stubber_client_directory()

    log_stream_name = "http_response/stream_file.json"
    add_describe_log_streams(stubber, log_group_name, log_stream_name, directory)

    log_stream_name = "uniquecode5678"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory)

    log_stream_name = "uniquecode1234"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory)

    return client, stubber


def generate_stubber_logs_with_existing_stream(
    log_group_name, log_group_name_existing, optional=None
):
    stubber, client, directory = stubber_client_directory()

    log_stream_name = log_group_name_existing
    add_describe_log_streams(stubber, log_group_name, log_stream_name, directory)

    log_stream_name = "http_response/stream_file.json"
    add_describe_log_streams(stubber, log_group_name, log_stream_name, directory)

    log_stream_name = "uniquecode5678"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory, optional)

    log_stream_name = "uniquecode1234"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory, optional)

    return client, stubber


def generate_stubber_logs_all_files_in_directory(
    log_group_name, log_group_name_existing, optional=None
):
    stubber, client, directory = stubber_client_directory()

    log_stream_name = log_group_name_existing
    add_describe_log_streams(stubber, log_group_name, log_stream_name, directory)

    log_stream_name = "uniquecode5678"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory, optional)

    log_stream_name = "uniquecode1234"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory, optional)

    log_stream_name = log_group_name_existing
    add_describe_log_streams(stubber, log_group_name, log_stream_name, directory)

    log_stream_name = "uniquecode5678"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory, optional)

    log_stream_name = "uniquecode1234"
    add_get_log_events(stubber, log_group_name, log_stream_name, directory, optional)

    return client, stubber

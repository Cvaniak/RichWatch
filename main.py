import boto3
from rich.console import Console
from other_tools.other import create_log_table
import sys


if __name__ == "__main__":
    log_name = "/aws/lambda/data-upload-lambda-receive-sqs-infra"

    region = None
    if len(sys.argv) == 3:
        region = sys.argv[-1]

    session = boto3.session.Session(reg)
    client = boto3.client("logs")
    console = Console()
    console.print(create_log_table(client, log_name))

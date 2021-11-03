from datetime import datetime

import boto3
from rich import box
from rich.console import Console
from rich.table import Table
from rich.text import Text
from other_tools.other import create_log_table


if __name__ == "__main__":
    log_name = "/aws/lambda/data-upload-lambda-receive-sqs-infra"

    client = boto3.client("logs")
    console = Console()
    console.print(create_log_table(client, log_name))

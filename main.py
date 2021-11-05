import boto3
from rich.console import Console
from other_tools.other import create_log_table


if __name__ == "__main__":
    log_name = "/aws/lambda/data-upload-lambda-receive-sqs-infra"

    client = boto3.client("logs")
    console = Console()
    console.print(create_log_table(client, log_name))

import boto3
from rich.console import Console
from other_tools.other import create_log_table
import sys


if __name__ == "__main__":

    region = dict()
    if len(sys.argv) == 3:
        region["region_name"] = sys.argv[-1]

    session = boto3.session.Session(**region)
    client = session.client("logs")
    console = Console()
    console.print(create_log_table(client, sys.argv[1]))

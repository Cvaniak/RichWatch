from rich import box, print
import boto3
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.json import JSON
from rich.highlighter import RegexHighlighter
from rich.pretty import Pretty
from datetime import datetime

client = boto3.client('logs')
log_name = "data-upload-lambda-receive-sqs-infra"


class RainbowHighlighter(RegexHighlighter):
    base_style = "aws."
    highlights = [r"(?P<error>\[ERROR\].+?(?=[:(Z )]))", r"(?P<errortext>\[ERROR\].*)",
                  r"(?P<start>START.+?(?=:))", r"(?P<info>\[INFO\].+?(?=Z))", r"(?P<report>REPORT.*)",
                  r"(?P<end>END.+?(?=:))"]


theme = Theme({"aws.error": "bold red",
               "aws.errortext": "red",
               "aws.start": "green",
               "aws.report": "dim yellow",
               "aws.info": "yellow",
               "aws.end": "cyan"})

console = Console(highlighter=RainbowHighlighter(), theme=theme)

# For the latest
stream_response = client.describe_log_streams(
    logGroupName=f"/aws/lambda/{log_name}",  # Can be dynamic
    orderBy='LastEventTime',                 # For the latest events
    descending=True,
    limit=2                                  # the last latest event, if you just want one
)

console.print(stream_response["logStreams"])
list_log_streams = stream_response["logStreams"]


table = Table(title=log_name, box=box.MINIMAL,
              show_lines=True, highlight=RainbowHighlighter())
table.add_column("Time")
table.add_column("Type")
table.add_column("Massage")
for log_detail in list_log_streams:
    response = client.get_log_events(
        logGroupName=f"/aws/lambda/{log_name}",
        logStreamName=log_detail["logStreamName"],
    )

    # console.print(response["events"])
    for event in response["events"]:
        # console.print(event["message"].replace("\t", "\n"), end="\n\n")
        d = datetime.fromtimestamp(event["timestamp"]/1000.0)
        time = d.strftime("%m/%d/%Y\n%H:%M:%S.%f")
        a = event["message"]
        # a = a.replace("\t", "\n")
        # while a.endswith("\n"):
        #     a = a[:-1]
        text = a.split(" ", 1)
        table.add_row(time, text[0], text[1])


console.print(table)

from rich import print
import boto3
from rich.console import Console
from rich.theme import Theme
from rich.json import JSON
from rich.highlighter import RegexHighlighter

client = boto3.client('logs')
log_name = "data-upload-lambda-receive-sqs-infra"


class RainbowHighlighter(RegexHighlighter):
    # def highlight(self, text):
    #     print(text)
    #     for index in range(len(text)):
    #         text.stylize(f"color({randint(16, 255)})", index, index + 1)
    base_style = "aws."
    # highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]
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
# latestlogStreamName = stream_response["logStreams"][0]["logStreamName"]


for log_detail in list_log_streams:
    response = client.get_log_events(
        logGroupName=f"/aws/lambda/{log_name}",
        logStreamName=log_detail["logStreamName"],
    )

    # console.print(response["events"])
    for event in response["events"]:
        console.print(event["message"].replace("\t", "\n"), end="\n\n")
#     if event["message"]["ClinicID"] == "7667":
#         print(event["message"])
#     elif event["message"]["username"] == "simran+test@abc.com":
#         print(event["message"])
#     # .
#     # .
#     # more if or else conditions

# # For more than one Streams, e.g. latest 5
# stream_response = client.describe_log_streams(
#     logGroupName="/aws/lambda/lambdaFnName",  # Can be dynamic
#     orderBy='LastEventTime',                 # For the latest events
#     limit=5
# )

# for log_stream in stream_response["logStreams"]:
#     latestlogStreamName = log_stream["logStreamName"]

#     response = client.get_log_events(
#         logGroupName="/aws/lambda/lambdaFnName",
#         logStreamName=latestlogStreamName,
#         startTime=12345678,
#         endTime=12345678,
#     )
#     # For example, you want to search "ClinicID=7667", can be dynamic

#     for event in response["events"]:
#         if event["message"]["ClinicID"] == "7667":
#             print(event["message"])
#         elif event["message"]["username"] == "simran+test@abc.com":
#             print(event["message"])
#         # .
#         # .
#         # more if or else conditions

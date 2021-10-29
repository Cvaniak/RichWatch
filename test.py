from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.live import Live
from time import sleep
from random import randint

from rich import print
from rich.highlighter import RegexHighlighter
from rich.console import Console
from rich.theme import Theme


class RainbowHighlighter(RegexHighlighter):
    # def highlight(self, text):
    #     print(text)
    #     for index in range(len(text)):
    #         text.stylize(f"color({randint(16, 255)})", index, index + 1)
    base_style = "aws."
    # highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]
    highlights = [r"(?P<error>[ERROR].*Z)",
                  r"(?P<start>START.*:)", r"(?P<info>[INFO].*Z)", r"(?P<info>REPORT.*:)",
                  r"(?P<end>END.*:)"]


theme = Theme({"aws.error": "bold red",
               "aws.start": "green",
               "aws.info": "yellow",
               "aws.end": "cyan"})
console = Console(highlighter=RainbowHighlighter(), theme=theme)
# print(rainbow("I must not fear. Fear is the mind-killer."))
console.print(
    "ERROR cos:. Fear is the mind-killer.money@example.org")
console.print(
    "START cos:. Fear is the mind-killer.money@example.org")
console.print(
    "INFO cos:. Fear is the mind-killer.money@example.org")
console.print(
    "REPORT cos:. Fear is the mind-killer.money@example.org")
console.print(
    "END cos:. fear is the mind-killer.money@example.org")
""


job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
job1 = job_progress.add_task("[green]Cooking")
job2 = job_progress.add_task("[magenta]Baking", total=200)
job3 = job_progress.add_task("[cyan]Mixing", total=400)

total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))

progress_table = Table.grid()
progress_table.add_row(
    Panel.fit(
        overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
    ),
    Panel.fit(job_progress, title="[b]Jobs",
              border_style="red", padding=(1, 2)),
)

with Live(progress_table, refresh_per_second=10):
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if not job.finished:
                job_progress.advance(job.id)

        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)

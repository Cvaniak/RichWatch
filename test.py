# flake8: noqa# neqa
# from rich.table import Table
# from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
# from rich.panel import Panel
# from rich.live import Live
# from time import sleep
# from random import randint

# from rich import print
# from rich.highlighter import RegexHighlighter
# from rich.console import Console
# from rich.theme import Theme


# class RainbowHighlighter(RegexHighlighter):
#     # def highlight(self, text):
#     #     print(text)
#     #     for index in range(len(text)):
#     #         text.stylize(f"color({randint(16, 255)})", index, index + 1)
#     base_style = "aws."
#     # highlights = [r"(?P<email>[\w-]+@([\w-]+\.)+[\w-]+)"]
#     highlights = [r"(?P<error>[ERROR].*Z)",
#                   r"(?P<start>START.*:)", r"(?P<info>[INFO].*Z)", r"(?P<info>REPORT.*:)",
#                   r"(?P<end>END.*:)"]


# theme = Theme({"aws.error": "bold red",
#                "aws.start": "green",
#                "aws.info": "yellow",
#                "aws.end": "cyan"})
# console = Console(highlighter=RainbowHighlighter(), theme=theme)
# # print(rainbow("I must not fear. Fear is the mind-killer."))
# console.print(
#     "ERROR cos:. Fear is the mind-killer.money@example.org")
# console.print(
#     "START cos:. Fear is the mind-killer.money@example.org")
# console.print(
#     "INFO cos:. Fear is the mind-killer.money@example.org")
# console.print(
#     "REPORT cos:. Fear is the mind-killer.money@example.org")
# console.print(
#     "END cos:. fear is the mind-killer.money@example.org")
# ""


# job_progress = Progress(
#     "{task.description}",
#     SpinnerColumn(),
#     BarColumn(),
#     TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
# )
# job1 = job_progress.add_task("[green]Cooking")
# job2 = job_progress.add_task("[magenta]Baking", total=200)
# job3 = job_progress.add_task("[cyan]Mixing", total=400)

# total = sum(task.total for task in job_progress.tasks)
# overall_progress = Progress()
# overall_task = overall_progress.add_task("All Jobs", total=int(total))

# progress_table = Table.grid()
# progress_table.add_row(
#     Panel.fit(
#         overall_progress, title="Overall Progress", border_style="green", padding=(2, 2)
#     ),
#     Panel.fit(job_progress, title="[b]Jobs",
#               border_style="red", padding=(1, 2)),
# )

# with Live(progress_table, refresh_per_second=10):
#     while not overall_progress.finished:
#         sleep(0.1)
#         for job in job_progress.tasks:
#             if not job.finished:
#                 job_progress.advance(job.id)

#         completed = sum(task.completed for task in job_progress.tasks)
#         overall_progress.update(overall_task, completed=completed)
# """
# Demonstrates a Rich "application" using the Layout and Live classes.
# """

# from time import sleep
# from rich.live import Live
# from datetime import datetime

# from rich import box
# from rich.align import Align
# from rich.console import Console, Group
# from rich.layout import Layout
# from rich.panel import Panel
# from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
# from rich.syntax import Syntax
# from rich.table import Table
# from rich.text import Text

# console = Console()


# def make_layout() -> Layout:
#     """Define the layout."""
#     layout = Layout(name="root")

#     layout.split(
#         Layout(name="header", size=3),
#         Layout(name="main", ratio=1),
#         Layout(name="footer", size=7),
#     )
#     layout["main"].split_row(
#         Layout(name="side"),
#         Layout(name="body", ratio=2, minimum_size=60),
#     )
#     layout["side"].split(Layout(name="box1"), Layout(name="box2"))
#     return layout


# def make_sponsor_message() -> Panel:
#     """Some example content."""
#     sponsor_message = Table.grid(padding=1)
#     sponsor_message.add_column(style="green", justify="right")
#     sponsor_message.add_column(no_wrap=True)
#     sponsor_message.add_row(
#         "Sponsor me",
#         "[u blue link=https://github.com/sponsors/willmcgugan]https://github.com/sponsors/willmcgugan",
#     )
#     sponsor_message.add_row(
#         "Buy me a :coffee:",
#         "[u blue link=https://ko-fi.com/willmcgugan]https://ko-fi.com/willmcgugan",
#     )
#     sponsor_message.add_row(
#         "Twitter",
#         "[u blue link=https://twitter.com/willmcgugan]https://twitter.com/willmcgugan",
#     )
#     sponsor_message.add_row(
#         "Blog", "[u blue link=https://www.willmcgugan.com]https://www.willmcgugan.com"
#     )

#     intro_message = Text.from_markup(
#         """Consider supporting my work via Github Sponsors (ask your company / organization), or buy me a coffee to say thanks. - Will McGugan"""
#     )

#     message = Table.grid(padding=1)
#     message.add_column()
#     message.add_column(no_wrap=True)
#     message.add_row(intro_message, sponsor_message)

#     message_panel = Panel(
#         Align.center(
#             Group(intro_message, "\n", Align.center(sponsor_message)),
#             vertical="middle",
#         ),
#         box=box.ROUNDED,
#         padding=(1, 2),
#         title="[b red]Thanks for trying out Rich!",
#         border_style="bright_blue",
#     )
#     return message_panel


# class Header:
#     """Display header with clock."""

#     def __rich__(self) -> Panel:
#         grid = Table.grid(expand=True)
#         grid.add_column(justify="center", ratio=1)
#         grid.add_column(justify="right")
#         grid.add_row(
#             "[b]Rich[/b] Layout application",
#             datetime.now().ctime().replace(":", "[blink]:[/]"),
#         )
#         return Panel(grid, style="white on blue")


# # def make_syntax() -> Syntax:
# #     code = """\
# def ratio_resolve(total: int, edges: List[Edge]) -> List[int]:
#     sizes = [(edge.size or None) for edge in edges]
#     # While any edges haven't been calculated
#     while any(size is None for size in sizes):
#         # Get flexible edges and index to map these back on to sizes list
#         flexible_edges = [
#             (index, edge)
#             for index, (size, edge) in enumerate(zip(sizes, edges))
#             if size is None
#         ]
#         # Remaining space in total
#         remaining = total - sum(size or 0 for size in sizes)
#         if remaining <= 0:
#             # No room for flexible edges
#             sizes[:] = [(size or 0) for size in sizes]
#             break
#         # Calculate number of characters in a ratio portion
#         portion = remaining / sum((edge.ratio or 1) for _, edge in flexible_edges)
#         # If any edges will be less than their minimum, replace size with the minimum
#         for index, edge in flexible_edges:
#             if portion * edge.ratio <= edge.minimum_size:
#                 sizes[index] = edge.minimum_size
#                 break
#         else:
#             # Distribute flexible space and compensate for rounding error
#             # Since edge sizes can only be integers we need to add the remainder
#             # to the following line
#             _modf = modf
#             remainder = 0.0
#             for index, edge in flexible_edges:
#                 remainder, size = _modf(portion * edge.ratio + remainder)
#                 sizes[index] = int(size)
#             break
#     # Sizes now contains integers only
#     return cast(List[int], sizes)
#     """
#     syntax = Syntax(code, "python", line_numbers=True)
#     return syntax


# job_progress = Progress(
#     "{task.description}",
#     SpinnerColumn(),
#     BarColumn(),
#     TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
# )
# job_progress.add_task("[green]Cooking")
# job_progress.add_task("[magenta]Baking", total=200)
# job_progress.add_task("[cyan]Mixing", total=400)

# total = sum(task.total for task in job_progress.tasks)
# overall_progress = Progress()
# overall_task = overall_progress.add_task("All Jobs", total=int(total))

# progress_table = Table.grid(expand=True)
# progress_table.add_row(
#     Panel(
#         overall_progress,
#         title="Overall Progress",
#         border_style="green",
#         padding=(2, 2),
#     ),
#     Panel(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
# )


# layout = make_layout()
# layout["header"].update(Header())
# layout["body"].update(make_sponsor_message())
# layout["box2"].update(Panel(make_syntax(), border_style="green"))
# layout["box1"].update(Panel(layout.tree, border_style="red"))
# layout["footer"].update(progress_table)


# with Live(layout, refresh_per_second=10, screen=True):
#     while not overall_progress.finished:
#         sleep(0.1)
#         for job in job_progress.tasks:
#             if not job.finished:
#                 job_progress.advance(job.id)

#         completed = sum(task.completed for task in job_progress.tasks)
#        # overall_progress.update(overall_task, completed=completed)
# from textual._easing import EASING
# from textual.app import App
# from textual.reactive import Reactive

# from textual.views import DockView
# from textual.widgets import Placeholder, TreeControl, ScrollView, TreeClick


# class EasingApp(App):
#     """An app do demonstrate easing."""

#     side = Reactive(False)
#     easing = Reactive("linear")

#     def watch_side(self, side: bool) -> None:
#         """Animate when the side changes (False for left, True for right)."""
#         width = self.easing_view.size.width
#         animate_x = (width - self.placeholder.size.width) if side else 0
#         self.placeholder.animate(
#             "layout_offset_x", animate_x, easing=self.easing, duration=1
#         )

#     async def on_mount(self) -> None:
#         """Called when application mode is ready."""

#         self.placeholder = Placeholder()
#         self.easing_view = DockView()
#         self.placeholder.style = "white on dark_blue"

#         self.tree = TreeControl("Easing", {})
#         for easing_key in sorted(EASING.keys()):
#             await self.tree.add(self.tree.root.id, easing_key, {"easing": easing_key})
#         await self.tree.root.expand()

#         await self.view.dock(ScrollView(self.tree), edge="left", size=32)
#         await self.view.dock(self.easing_view)
#         await self.easing_view.dock(self.placeholder, edge="left", size=32)

#     async def handle_tree_click(self, message: TreeClick[dict]) -> None:
#         """Called in response to a tree click."""
#         self.easing = message.node.data.get("easing", "linear")
#         self.side = not self.side


# EasingApp().run(log="textual.log")
from textual.widgets import Placeholder
from textual import events
from rich.status import Status
from rich.console import Console
import os
import sys
from rich.console import RenderableType

from rich.syntax import Syntax
from rich.traceback import Traceback

from textual.app import App
from textual.widgets import Header, Footer, FileClick, ScrollView, DirectoryTree


class MyApp(App):
    """An example of a very simple Textual App"""

    async def on_load(self) -> None:
        """Sent before going in to application mode."""

        # Bind our basic keys
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

        # Get path to show
        try:
            self.path = sys.argv[1]
        except IndexError:
            self.path = os.path.abspath(
                os.path.join(os.path.basename(__file__), "../../")
            )

    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""

        # Create our widgets
        # In this a scroll view for the code and a directory tree
        self.body = ScrollView()
        self.directory = DirectoryTree(self.path, "Code")

        # Dock our widgets
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")

        # Note the directory is also in a scroll view
        await self.view.dock(
            ScrollView(self.directory), edge="left", size=48, name="sidebar"
        )
        await self.view.dock(self.body, edge="top")

    async def handle_file_click(self, message: FileClick) -> None:
        """A message sent by the directory tree when a file is clicked."""

        syntax: RenderableType
        try:
            # Construct a Syntax object for the path in the message
            syntax = Syntax.from_path(
                message.path,
                line_numbers=True,
                word_wrap=True,
                indent_guides=True,
                theme="monokai",
            )
        except Exception:
            # Possibly a binary file
            # For demonstration purposes we will show the traceback
            syntax = Traceback(theme="monokai", width=None, show_locals=True)
        self.app.sub_title = os.path.basename(message.path)
        await self.body.update(syntax)


# Run our app class
# MyApp.run(title="Code Viewer", log="textual.log")
# console = Console()
# console.print(Status("test"))


class GridTest(App):
    async def on_mount(self, event: events.Mount) -> None:
        """Create a grid with auto-arranging cells."""

        grid = await self.view.dock_grid()

        grid.add_column("col", fraction=1, max_size=20)
        grid.add_row("row", fraction=1, max_size=10)
        grid.set_repeat(True, True)
        grid.add_areas(center="col-2-start|col-4-end,row-2-start|row-3-end")
        grid.set_align("stretch", "center")

        placeholders = [Placeholder() for _ in range(20)]
        grid.place(*placeholders, center=Placeholder())


# GridTest.run(title="Grid Test", log="textual.log")
import shlex
import subprocess
import sys

from rich.console import Console

DOWN_TRIANGLE = "\u25BC"


class CommandProcessor:
    def __init__(self, commands):
        self.commands = commands

    def run(self):
        console = Console()

        for name, command in self.commands.items():
            console.print()
            console.rule(f"{DOWN_TRIANGLE} [bold blue]{name.lower()}", align="left")
            console.print(f"[bold yellow]{command}[/]")
            command_split = shlex.split(command)
            result = subprocess.run(command_split)
            if result.returncode:
                console.print(
                    f"\n[bold red]Error:exclamation:[/] in [bold blue]{name} ([bold yellow]{command}[/])[/]"
                )
                sys.exit(result.returncode)


if __name__ == "__main__":
    test_commands = {"list files": "ls .", "testing echo": "echo 'hello world'"}
    command_processor = CommandProcessor(test_commands)
    command_processor.run()

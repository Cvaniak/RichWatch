from rich import box
import rich
from rich.align import Align
from rich.console import RenderableType
from rich.pretty import Pretty
from rich.segment import Segment
from rich.table import Table
from textual.widgets import Placeholder, TreeControl, ScrollView, TreeClick
from textual.views import DockView
from textual._easing import EASING
from rich.markdown import Markdown

from textual import events
from textual.app import App
from textual.widgets import Header, Footer, Placeholder, ScrollView
from rich.panel import Panel
from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
import time
import boto3
from main import *
import threading


def log_get(log_name):
    # if log_name is None:
    #     log_name = self.log_name
    client = boto3.client('logs')
    stream_response = client.describe_log_streams(
        logGroupName=f"/aws/lambda/{log_name}",  # Can be dynamic
        orderBy='LastEventTime',                 # For the latest events
        descending=True,
        limit=2                                  # the last latest event, if you just want one
    )


print(log_get())
# threads = []

# t = threading.Thread(target=log_get, args=[log_name])
# threads.append(t)
# t.start()

# console.print(stream_response["logStreams"])
# list_log_streams = stream_response["logStreams"]

# table = Table(title=log_name, box=box.MINIMAL,
#               show_lines=True, highlight=None)
# table.add_column("Time")
# table.add_column("Type")
# table.add_column("Massage")
# for log_detail in list_log_streams:
#     response = client.get_log_events(
#         logGroupName=f"/aws/lambda/{log_name}",
#         logStreamName=log_detail["logStreamName"],
#     )

#     # console.print(response["events"])
#     for event in response["events"]:
#         # console.print(event["message"].replace("\t", "\n"), end="\n\n")

#         table.add_row(*format_event(event))

# return table
# self.table = table

...


class Hover(Widget):
    has_focus = Reactive(False)
    mouse_over = Reactive(False)
    style = Reactive("")
    height = Reactive(None)
    text = "Lorem Ipsum"
    log_name = "data-upload-lambda-receive-sqs-infra"
    table = Table()

    def __init__(self, *, name=None, height=None) -> None:
        super().__init__(name=name)
        self.height = height

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", self.name
        yield "has_focus", self.has_focus, False
        yield "mouse_over", self.mouse_over, False

    def render(self) -> RenderableType:
        # p = await self.load_logs()

        # t = Table()
        # t.add_column("a")
        # t.add_column("b")
        # t.add_row("c", "c1")
        # t.add_row("d", "d1")
        # t1 = self.load_logs()
        # p = f"{type(t)}, {type(t1)}"
        return Panel(
            # Table(Pretty("test")),
            # self.load_logs(),
            # Align.center(
            self.table,
            # Segment("test"),
            # Segment(self.text),
            # Pretty(self.text, no_wrap=True, overflow="ellipsis"), vertical="middle"
            # ),
            title=self.__class__.__name__,
            border_style="green" if self.mouse_over else "blue",
            box=box.HEAVY if self.has_focus else box.ROUNDED,
            style=self.style,
            height=self.height,
        )

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True
        for i in threads:
            i.start()

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_enter(self, event: events.Enter) -> None:
        self.mouse_over = True

    async def on_leave(self, event: events.Leave) -> None:
        self.mouse_over = False

    async def load_logs(self, log_name=None):
        if log_name is None:
            log_name = self.log_name
        client = boto3.client('logs')
        stream_response = client.describe_log_streams(
            logGroupName=f"/aws/lambda/{log_name}",  # Can be dynamic
            orderBy='LastEventTime',                 # For the latest events
            descending=True,
            limit=2                                  # the last latest event, if you just want one
        )

        # console.print(stream_response["logStreams"])
        # list_log_streams = stream_response["logStreams"]

        # table = Table(title=log_name, box=box.MINIMAL,
        #               show_lines=True, highlight=None)
        # table.add_column("Time")
        # table.add_column("Type")
        # table.add_column("Massage")
        # for log_detail in list_log_streams:
        #     response = client.get_log_events(
        #         logGroupName=f"/aws/lambda/{log_name}",
        #         logStreamName=log_detail["logStreamName"],
        #     )

        #     # console.print(response["events"])
        #     for event in response["events"]:
        #         # console.print(event["message"].replace("\t", "\n"), end="\n\n")

        #         table.add_row(*format_event(event))

        # return table
        # self.table = table


class MyApp(App):
    """An example of a very simple Textual App"""

    async def fill(self):
        # await time.sleep(3)
        await self.body.update("Test from bind")

    async def action_test(self):
        ...
        # await self.call_later(get_markdown, "richreadme.md")
        await self.call_later(self.fill)

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("l", "test", "Toggle sidebar")
        await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")

    async def on_mount(self, event: events.Mount) -> None:
        """Create and dock the widgets."""

        # A scrollview to contain the markdown file
        self.body = ScrollView(gutter=1)
        self.list = ScrollView(gutter=1)

        # Header / footer / dock
        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        # Dock the body in the remaining space
        # hovers = (Hover() for _ in range(3))

        self.tree = TreeControl("List of Logs Groups", {})

        async def get_lambdas(filename: str) -> None:
            with open(filename, "rt") as fh:
                lines = fh.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    await self.tree.add(self.tree.root.id, line, {"group_name": line})
            await self.tree.root.expand()

        # for easing_key in ["a", "b", "c", "d", "e", "f"]:
        #     # await tree.add(tree.root.id, easing_key, {"easing": easing_key})
        #     await self.tree.add(self.tree.root.id, easing_key, {"my_data": easing_key})
        # await self.tree.root.expand()

        self.hover = Hover()

        await self.view.dock(ScrollView(self.tree), edge="left", size=30, name="sidebar")
        await self.view.dock(Placeholder(), edge="right", size=30)
        await self.view.dock(self.hover)
        # await self.view.dock(self.hover)
        await get_lambdas("test.txt")

        async def handle_tree_click(self, message: TreeClick[dict]) -> None:
            """Called in response to a tree click."""
            await self.tree.root.expand()
        # hovers = (Hover() for _ in range(3))
        # await self.view.dock(*hovers, edge="top")

        # async def get_markdown(filename: str) -> None:
        #     with open(filename, "rt") as fh:
        #         readme = Markdown(fh.read(), hyperlinks=True)
        # await self.body.update("Test")

        # async def get_markdown(filename: str) -> None:
        #     with open(filename, "rt") as fh:
        #         readme = Markdown(fh.read(), hyperlinks=True)
        #     await body.update(readme)

        # await self.call_later(self.test)


# MyApp.run(screen=False, title="Simple App", log="textual.log")
# class GridTest(App):
#     async def action_test(self):
#         ...
#         # self.grid.place()

#     async def on_load(self, event: events.Load) -> None:
#         """Bind keys with the app loads (but before entering application mode)"""
#         await self.bind("l", "test", "Toggle sidebar")

#     async def on_mount(self) -> None:
#         """Make a simple grid arrangement."""

#         grid = await self.view.dock_grid(edge="left", name="left")

#         grid.add_column(fraction=1, name="left", min_size=20)
#         grid.add_column(size=30, name="center")
#         grid.add_column(fraction=1, name="right")

#         grid.add_row(fraction=1, name="top", min_size=2)
#         grid.add_row(fraction=2, name="middle")
#         grid.add_row(fraction=1, name="bottom")

#         grid.add_areas(
#             area1="left,top",
#             area2="center,middle",
#             area3="left-start|right-end,bottom",
#             area4="right,top-start|middle-end",
#         )

#         grid.place(
#             area1=Placeholder(name="area1"),
#             area2=Placeholder(name="area2"),
#             area3=Placeholder(name="area3"),
#             area4=Placeholder(name="area4"),
#         )
#         grid.place(Placeholder())
#         grid.place(Placeholder())


# GridTest.run(title="Grid Test", log="textual.log")


class EasingApp(App):
    """An app do demonstrate easing."""

    side = Reactive(False)
    easing = Reactive("linear")
    abcd = Reactive("This is test")

    # def watch_side(self, side: bool) -> None:
    #     """Animate when the side changes (False for left, True for right)."""
    #     width = self.easing_view.size.width
    #     animate_x = (width - self.placeholder.size.width) if side else 0
    #     self.placeholder.animate(
    #         "layout_offset_x", animate_x, easing=self.easing, duration=1
    #     )

    async def watch_abcd(self, abcd):
        ...
        await self.tree.add(self.tree.root.id, "w", {"my_data": "w"})

    async def on_mount(self) -> None:
        """Called when application mode is ready."""

        self.placeholder = Placeholder(height=8)
        self.placeholder1 = Placeholder(height=8)
        self.easing_view = DockView()
        self.placeholder.style = "black on cyan"
        self.placeholder1.style = "white on dark_blue"

        self.tree = TreeControl("Easing", {})
        for easing_key in ["a", "b", "c", "d", "e", "f"]:
            # await tree.add(tree.root.id, easing_key, {"easing": easing_key})
            await self.tree.add(self.tree.root.id, easing_key, {"my_data": easing_key})
        await self.tree.root.expand()

        await self.view.dock(ScrollView(self.tree), edge="left", size=32)
        await self.view.dock(ScrollView(self.easing_view), edge="right", size=32)
        grid = await self.easing_view.dock_grid()
        await self.easing_view.dock(self.placeholder1)
        await self.easing_view.dock(self.placeholder)
        # grid.add_row()
        # grid.add_row()
        grid.add_row(name="a")
        grid.add_row(name="b")
        grid.add_column(name="d")
        grid.place(Placeholder())
        grid.place(Placeholder())
        # self.abcd = message.node.data.get("my_data", "z")
        # self.easing = message.node.data.get("easing", "linear")
        # self.side = not self.side

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        """Called in response to a tree click."""
        await self.tree.root.expand()


# EasingApp().run(log="textual.log")

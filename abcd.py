from rich import box
import rich
from rich.align import Align
from rich.console import RenderableType
from rich.pretty import Pretty
from rich.segment import Segment
from rich.table import Table
from textual.message import Message
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
import sys

import boto3
import boto3.session
import threading

eve = threading.Event()
threads = []
datas = []
log_group = []


class MyTask(threading.Thread):
    def run(self):
        while True:
            if eve.is_set():
                session = boto3.session.Session()
                client = session.client("logs")
                datas.append(create_log_table(client, log_group[-1]))
                eve.clear()


t = MyTask()
t.start()


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
        return Panel(
            "\n" * 100 if not len(datas) else datas[-1],
            title=self.__class__.__name__,
            border_style="green" if self.mouse_over else "blue",
            box=box.HEAVY if self.has_focus else box.ROUNDED,
            style=self.style,
            height=self.height,
        )

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_enter(self, event: events.Enter) -> None:
        self.mouse_over = True

    async def on_leave(self, event: events.Leave) -> None:
        self.mouse_over = False


class MyApp(App):
    """An example of a very simple Textual App"""

    async def fill(self, value):
        await self.body.update(value)

    async def action_test(self):
        await self.scrollview.handle_window_change(Message("Message"))
        self.scrollview.refresh()
        self.refresh()
        self.hover.refresh()
        # self.scrollview.virtual_size = 10
        # await self.call_later(get_markdown, "richreadme.md")
        # self.refresh()
        # await self.call_later(self.fill)

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        await self.bind("l", "test", "Refresh")
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

        tree = TreeControl("List of Logs Groups", data={})
        self.tree = tree

        async def get_lambdas(filename: str) -> None:
            with open(filename, "rt") as fh:
                lines = fh.readlines()
                for line in lines:
                    line = line.replace("\n", "")
                    await self.tree.add(self.tree.root.id, line, {"group_name": line})
            await self.tree.root.expand()

        self.hover = Hover()
        self.scrollview = ScrollView(self.hover)

        await self.view.dock(
            ScrollView(self.tree), edge="left", size=30, name="sidebar"
        )
        await self.view.dock(Placeholder(), edge="right", size=30)
        await self.view.dock(self.scrollview)
        await get_lambdas("test.txt")

    async def handle_tree_click(self, message: TreeClick[dict]) -> None:
        """Called in response to a tree click."""
        action = message.node.data.get("group_name", None)
        if action is not None and not eve.is_set():
            log_group.append(action)
            eve.set()


MyApp.run(title="Simple App", log="textual.log")
